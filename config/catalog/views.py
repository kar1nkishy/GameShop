from django.shortcuts import get_object_or_404, render
from .models import Game, Genre, GameImage
from django.core.paginator import Paginator
from django.db.models import Q
from decimal import Decimal, InvalidOperation

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

def product_list_by_category(request, slug):
    catalog_obj = get_object_or_404(Genre, slug=slug)
    qs = Game.objects.filter(genre=catalog_obj)

    # Оптимизация
    qs = qs.select_related("genre").prefetch_related("images")

    # Поиск
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    # Фильтр по цене
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    try:
        if min_price:
            qs = qs.filter(price__gte=Decimal(min_price))
        if max_price:
            qs = qs.filter(price__lte=Decimal(max_price))
    except (InvalidOperation, ValueError):
        pass

    # Сортировка
    sort = request.GET.get("sort", "")
    if sort == "price_asc":
        qs = qs.order_by("price")
    elif sort == "price_desc":
        qs = qs.order_by("-price")
    elif sort == "new":
        qs = qs.order_by("-id")
    else:
        qs = qs.order_by("name")

    # Пагинация
    paginator = Paginator(qs, 8)
    page_obj = paginator.get_page(request.GET.get("page"))

    params = request.GET.copy()
    params.pop("page", None)
    qs_params = params.urlencode()

    return render(request, "catalog/product_list.html", {
        "catalog": catalog_obj,
        "page_obj": page_obj,
        "qs_params": qs_params,
    })






