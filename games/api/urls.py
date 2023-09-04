from django.urls import path
from games.api import views
app_name = 'games_api'

urlpatterns = [
    path('userdata/<str:user_id>', views.UserData.as_view(), name='user_data'),
    path('countreviews/<str:start_date>&<str:end_date>', views.CountReviews.as_view(), name='count_reviews'),
    path('genre/<str:genre>', views.Genre.as_view(), name='genre'),
    path('userforgenre/<str:genre>', views.UserForGenre.as_view(), name='userforgenre'),
    path('developer/<str:developer>', views.Developer.as_view(), name='developer'),
    path('sentiment/<str:year>', views.SentimentAnalisys.as_view(), name='sentiment'),
    path('recommend/<int:game_id>', views.Recommendation.as_view(), name='recommendation0'),
]