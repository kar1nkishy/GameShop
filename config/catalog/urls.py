from django.urls import path
from . import views

urlpatterns = [
    path ("", views.index, name='index'),
    path("genres/", views.genre_list, name="genre_list"),
    path("category/<slug:slug>/", views.product_list_by_category, name="product_list_by_category"),
    path("game/<slug:slug>/", views.game_detail, name="game_detail"),
]
