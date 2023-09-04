from django.contrib import admin
from games import models
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('user_id', 'steam_id', 'items_count', 'user_url')
    list_display = ('user_id', 'items_count')

class GameAdmin(admin.ModelAdmin):
    readonly_fields = ('game_id', 'name')
    list_display = ('game_id', 'name')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SpecAdmin(admin.ModelAdmin):
    list_display = ('name',)

class GameInfoAdmin(admin.ModelAdmin):
    list_display = ('game', 'price','release_date','developer')

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Game, GameAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Spec, SpecAdmin)
admin.site.register(models.GameInfo, GameInfoAdmin)
