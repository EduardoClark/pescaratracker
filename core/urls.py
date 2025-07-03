from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('player/<int:player_id>/', views.player_detail, name='player_detail'),
    path('league/', views.league_table, name='league_table'),

]