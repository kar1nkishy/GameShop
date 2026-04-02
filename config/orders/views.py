from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Order, OrderItem
from catalog.models import Game

@require_http_methods(["GET", "POST"])
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        # Создать заказ
        order = Order.objects.create(
            full_name=full_name,
            phone=phone,
            address=address,
        )
        
        # Если пользователь авторизован, привязать заказ к нему
        if request.user.is_authenticated:
            order.user = request.user
            order.save(update_fields=['user'])
        
        # Создать OrderItems
        for game_id, qty in cart.items():
            game = get_object_or_404(Game, id=int(game_id))
            for _ in range(qty):
                OrderItem.objects.create(
                    order=order,
                    game=game,
                    price=game.price,
                )
        
        # Очистить корзину
        request.session['cart'] = {}
        request.session.modified = True
        
        return redirect('order_detail', order_id=order.id)
    
    return render(request, 'orders/checkout.html')

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.orderitem_set.all()
    total_sum = sum(item.price for item in items)
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items,
        'total_sum': total_sum,
    })
