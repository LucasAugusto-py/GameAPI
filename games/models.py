from django.db import models
from datetime import datetime
from django.db.models import Sum, Count
# Create your models here.
    
class Game(models.Model):
    game_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='Título')

    class Meta:
        verbose_name = 'Juego'
        verbose_name_plural = 'Juegos'

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Género')
    
    class Meta:
        verbose_name = 'género'
        verbose_name_plural = 'géneros'
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Tag')

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name
    
class Spec(models.Model):
    name = models.CharField(max_length=200, verbose_name='Especificaciones')

    class Meta:
        verbose_name = 'spec'
        verbose_name_plural = 'specs'

    def __str__(self):
        return self.name
    
class GameInfo(models.Model):
    game = models.OneToOneField(
        Game,
        on_delete=models.CASCADE,
        primary_key=True
    )
    price = models.IntegerField(verbose_name='Precio', null=True)
    release_date = models.DateField(verbose_name='Fecha de salida', null=True)
    publisher = models.CharField(verbose_name='Editor', max_length=200, null=True)
    developer = models.CharField(verbose_name='Desarrollador', max_length=200, null=True)
    url = models.URLField(verbose_name='Url al juego')
    early_access = models.BooleanField(verbose_name='¿Acceso anticipado?')
    genres = models.ManyToManyField(Genre, verbose_name='Géneros')
    specs = models.ManyToManyField(Spec, verbose_name='Especificaciones')
    tags = models.ManyToManyField(Tag, verbose_name='Tags')

    class Meta:
        verbose_name ='Detalles de juego'
        verbose_name_plural = 'Detalles de juegos'
        
    @staticmethod
    def playtime_by_genre(genre_name):
        try:
            games_in_genre = UserGamePlaytime.objects.filter(game__gameinfo__genres__name=genre_name)
            total_hours = 0
            for game in games_in_genre:
                total_hours += game.playtime_hours
            return total_hours

        except UserGamePlaytime.DoesNotExist:
            return 0
    
    @staticmethod
    def free_content_by_developer(publisher_name):
        try:
            publisher = GameInfo.objects.filter(publisher=publisher_name)
            years = publisher.values_list('release_date__year', flat=True).distinct()
            results_by_year = {}
            for year in years:
                game_by_year = publisher.filter(release_date__year=year)
                total_games = game_by_year.count()
                free_games = game_by_year.filter(price=0).count()

                percentage_free = (free_games / total_games) * 100 if total_games > 0 else 0
                results_by_year[year] = f'{int(percentage_free)}%'
            return results_by_year
        except GameInfo.DoesNotExist:
            return {}
        


class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=200)
    steam_id = models.BigIntegerField()
    items_count = models.IntegerField(verbose_name='Cantidad de Juegos')
    user_url = models.URLField(verbose_name='Link al usuario')
    games = models.ManyToManyField(Game)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.user_id
    
    def total_playtime(self):
        total_hours = 0
        user_playtimes = UserGamePlaytime.objects.filter(user_id=self.user_id)
        for playtime_entry in user_playtimes:
            total_hours += playtime_entry.playtime_hours
        return total_hours
    
    def total_spent(self):
        total = 0
        for game in self.games.all():
            try:
                game_info = GameInfo.objects.get(game=game)
                if isinstance(game_info.price, int):
                    total += game_info.price
            except GameInfo.DoesNotExist:
                pass
        return f'{total} U$D'
    
    def recommend_porcentage(self):
        reviews = UserReviews.objects.filter(user_id = self.user_id)
        if len(reviews) == 0:
            return 'User has no reviews'
        recommends = 0
        for review in reviews:
            if review.recommend == True:
                recommends += 1
        return f'{int((recommends / len(reviews)) * 100)}%'
    

class UserGamePlaytime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    playtime_hours = models.IntegerField(verbose_name='Horas jugadas', default=0)

    class Meta:
        verbose_name = 'Tiempo de juego por usuario'
        verbose_name_plural = 'Tiempos de juego por usuarios'

    def __str__(self):
        return f'{self.user.user_id} - {self.game.name} - {self.playtime_hours} horas'
    
    @staticmethod
    def top_user_by_genre(genre_name):     
        try:
            top_users = UserGamePlaytime.objects.filter(game__gameinfo__genres__name=genre_name).values('user_id').annotate(total_playtime=Sum('playtime_hours')).order_by('-total_playtime')[:5]
            return top_users
        
        except UserGamePlaytime.DoesNotExist:
            return []

class UserReviews(models.Model):
    user = models.ForeignKey(User, verbose_name='Usuario de la reseña', null=True, on_delete=models.CASCADE)
    funny = models.CharField(verbose_name='Divertido',max_length=200, null=True)
    posted = models.DateField(verbose_name='Posteado', null=True)
    last_edited = models.CharField(verbose_name='Ultima vez editado', max_length=200, null=True)
    game = models.ForeignKey(Game, verbose_name='Juego de la reseña', null=True, on_delete=models.CASCADE)
    helpful = models.CharField(verbose_name='Fue de ayuda?', max_length=200, null=True)
    recommend = models.BooleanField(verbose_name='Recomendado?', null=True)
    review = models.TextField(verbose_name='Reseña', null=True)

    def __str__(self):
        return f'Reseña del usuario {self.user_id}'
    
    class Meta:
        verbose_name = 'Reseña de usuario'
        verbose_name_plural = 'Reseñas de usuarios'

    @staticmethod
    def user_count_and_user_recomend(start_date, end_date):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        reviews = UserReviews.objects.filter(
            posted__gte=start_date,
            posted__lte=end_date
        )

        users = set([review.user_id for review in reviews])

        user_recommend = 0
        for review in reviews:
            if review.recommend == True:
                user_recommend += 1

        return len(users), f'{int(round(user_recommend/len(reviews), 2)*100)}%'
    