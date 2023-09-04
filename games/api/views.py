from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from games import models
from django.db.models import Sum
from scipy.sparse import load_npz
tfidf_matrix = load_npz(r'E:\Documents\Code\PROYECTOS\PI_MLOps-STEAMv2\games\static\matrix\tfidf_matrix.npz')
import nltk 
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
import pandas as pd
df = pd.read_csv('data/csv/games_to_recommend.csv')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class UserData(APIView):
    '''
     Debe devolver cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.
    '''
    def get(self, response, user_id):
        user = models.User.objects.get(user_id=user_id)
        data = {
            'user_id': user.user_id,
            'total_games': user.items_count,
            'total_spent': user.total_spent(),
            'recommend_percentage':user.recommend_porcentage()
        
        }
        return Response(status=status.HTTP_200_OK, data=data)

class CountReviews(APIView):
    '''Cantidad de usuarios que realizaron reviews entre las fechas dadas y, el porcentaje de recomendación de los mismos en base a reviews.recommend.'''

    def get(self, response, start_date, end_date):
        user_count, user_recommend = models.UserReviews.user_count_and_user_recomend(start_date, end_date)
        data = {
            'user_count':user_count,
            'user_recommend_porcentage': user_recommend
        }
        return Response(status=status.HTTP_200_OK, data=data)
    
class Genre(APIView):
    '''Devuelve el puesto en el que se encuentra un género sobre el ranking de los mismos analizado bajo la columna PlayTimeForever.'''

    def get(self, response, genre):
        top_genres = models.UserGamePlaytime.objects.values('game__gameinfo__genres__name').annotate(hours=Sum('playtime_hours')).order_by('-hours')
        rank = None

        for index, item in enumerate(top_genres, start=1):
            if item['game__gameinfo__genres__name'] == genre:
                rank = index
        if rank is not None:
            return Response(status=status.HTTP_200_OK, data={
                genre:rank
            })
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'error':f'not fount {genre} genre'
            })

class UserForGenre(APIView):
    def get(self, request, genre):
        return Response(status=status.HTTP_200_OK, data={
            'top_5_users': models.UserGamePlaytime.top_user_by_genre(genre)
        })

class Developer(APIView):
    def get(self, request, developer):
        return Response(status=status.HTTP_200_OK, data=models.GameInfo.free_content_by_developer(developer))

class SentimentAnalisys(APIView):
    def get(self, request, year):
        data = models.UserReviews.objects.filter(posted__year=year).values('review')
        data = [i['review'] for i in data]
        sentiment = {
            'Negative':0,
            'Mixed':0,
            'Positive':0
        }
        for review in data:
            compound = sia.polarity_scores(review)['compound']
            if compound > 0:
                sentiment['Positive'] += 1
            elif compound < 0:
                sentiment['Negative'] += 1
            else:
                sentiment['Mixed'] += 1
            

        return Response(status=status.HTTP_200_OK, data=sentiment)
    
class Recommendation(APIView):
    def get(self, request, game_id):
        game_title = models.Game.objects.get(pk=game_id).name
        title = game_title.lower()
        game_index = df[df['title'].str.lower() == title].index.values
        if len(game_index) > 0:
            similarity = cosine_similarity(
                tfidf_matrix[game_index],
                tfidf_matrix
            )
            similar_games_index = similarity.argsort()[0][-6:][::-1]
            similar_games = df.iloc[similar_games_index]
            game_index = similar_games[similar_games['title'].str.lower() == title].index.values
            if len(game_index) > 0:
                similar_games.drop(index=game_index, inplace=True)
            else:
                similar_games.drop(similar_games.index[-1], inplace=True)
            list_games =  list(similar_games['game_id'])
            games_obj = models.Game.objects.filter(game_id__in=list_games).values('game_id','name')

            return Response(status=status.HTTP_200_OK, data={
                'Similar Games': games_obj
            })
    
