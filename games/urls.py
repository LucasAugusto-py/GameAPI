from django.urls import path, include
from games import views

app_name = 'games'

urlpatterns = [
    path('api/', include('games.api.urls')),
    path('', views.GameListView.as_view(), name='game_list'),
    path('detail/<int:pk>/<slug:slug>/', views.GameDetailView.as_view(), name='game_detail'),
]