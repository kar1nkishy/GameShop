from django.shortcuts import get_object_or_404, render, redirect
from .models import Game, Genre, GameImage
from django.core.paginator import Paginator
from django.db.models import Q
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse

def index(request):
    genres = Genre.objects.all()
    games = Game.objects.all().order_by('-id')[:10]  # последние 10 игр
    return render(request, "index.html", {"genres": genres, "games": games})

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
    genre_obj = get_object_or_404(Genre, slug=slug)
    qs = Game.objects.filter(genre=genre_obj)

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

    return render(request, "game_list.html", {
        "genre": genre_obj,
        "page_obj": page_obj,
        "qs_params": qs_params,
    })

def add_to_cart(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    cart = request.session.get('cart', {})
    game_id_str = str(game_id)
    current_qty = cart.get(game_id_str, 0)
    cart[game_id_str] = current_qty + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def remove_from_cart(request, game_id):
    cart = request.session.get('cart', {})
    game_id_str = str(game_id)
    if game_id_str in cart:
        del cart[game_id_str]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')

def update_cart(request, game_id, action):
    game = get_object_or_404(Game, id=game_id)
    cart = request.session.get('cart', {})
    game_id_str = str(game_id)
    current_qty = cart.get(game_id_str, 0)
    if action == 'increase':
        cart[game_id_str] = current_qty + 1
    elif action == 'decrease':
        if current_qty > 1:
            cart[game_id_str] = current_qty - 1
        else:
            del cart[game_id_str]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

def cart_view(request):
    cart = request.session.get('cart', {})
    games = []
    total_sum = 0
    total_items = 0
    total_quantity = 0
    for game_id, qty in cart.items():
        game = get_object_or_404(Game, id=int(game_id))
        subtotal = game.price * qty
        total_sum += subtotal
        total_items += 1
        total_quantity += qty
        games.append({
            'game': game,
            'quantity': qty,
            'subtotal': subtotal,
        })
    return render(request, 'cart.html', {
        'games': games,
        'total_sum': total_sum,
        'total_items': total_items,
        'total_quantity': total_quantity,
    })






