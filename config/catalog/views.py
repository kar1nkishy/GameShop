from django.shortcuts import get_object_or_404, render
from .models import Game, Genre, GameImage
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    genres = Genre.objects.all()
    return render(request, "index.html", {"genres": genres})

def genre_list(request):
    genres = Genre.objects.all()
    return render(request, "genre_list.html", {"genres": genres})

def game_list_by_genre(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    qs = Game.objects.filter(genre=genre).order_by("name")

def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug)
    return render(request, "game_detail.html", {"game": game})

def game_list_by_genre(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    qs = Game.objects.filter(genre=genre)
    qs = qs.select_related("genre").prefetch_related("images")
    q = request.GET.get("q", "").strip()

    if q:
       qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    paginator = Paginator(qs, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "game_list.html", {
        "genre": genre,
        "page_obj": page_obj,
    })






