from django.urls import path
from . import views

urlpatterns = [
    path ("", views.index, name='index'),
    path("genres/", views.genre_list, name="genre_list"),
    path("genre/<slug:slug>/", views.game_list_by_genre, name="game_list_by_genre"),
    path("game/<slug:slug>/", views.game_detail, name="game_detail"),
    path("add_to_cart/<int:game_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart/<int:game_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("update_cart/<int:game_id>/<str:action>/", views.update_cart, name="update_cart"),
    path("cart/", views.cart_view, name="cart"),
]
