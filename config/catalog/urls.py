from django.urls import path
from . import views

urlpatterns = [
    path ('', views.index, name='index'),
    path("genres/", views.genre_list, name="genre_list"),
    path("genre/<slug:slug>/", views.game_list_by_genre, name="game_list_by_genre"),
    path("game/<slug:slug>/", views.game_detail, name="game_detail"),
]
