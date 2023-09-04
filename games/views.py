from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from games import models
# Create your views here.
class GameListView(ListView):
    model = models.Game

    def get_queryset(self):
        return models.Game.objects.all().order_by('game_id')[:10]
    
class GameDetailView(DetailView):
    model = models.GameInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        game_info = self.object

        context['game'] = game_info.game

        return context



