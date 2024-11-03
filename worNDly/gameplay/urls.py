from django.urls import path
from . import views

app_name='gameplay'
urlpatterns = [
    path('start_game/', views.start_game, name='start_game'),
    path('start_game_ENGLISH', views.start_game_ENGLISH, name='start_game_ENGLISH'),
    path('start_game_GERMAN', views.start_game_GERMAN, name='start_game_GERMAN'),
    path('start_game_SPANISH', views.start_game_SPANISH, name='start_game_SPANISH'),
    path('start_game_PORT', views.start_game_PORT, name='start_game_PORT'),
    path('start_game_FRENCH', views.start_game_FRENCH, name='start_game_FRENCH'),
    path('desired_lang/', views.desired_lang, name='desired_lang')
]
