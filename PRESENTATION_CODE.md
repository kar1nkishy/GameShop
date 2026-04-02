# 🎮 Game Shop — Итоговый Проект

**Веб-магазин видеоигр**  
*Самое важное*

---

## 📊 Модели данных

**Game & Genre:**
```python
class Game(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
```

**Order & OrderItem:**
```python
class Order(models.Model):
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    game = models.ForeignKey(Game)
    price = models.DecimalField(max_digits=8, decimal_places=2)
```

→ Жанры, игры и скриншоты в БД. Заказы создаются с товарами.

---

## 🔧 Главная логика (Views)

**Добавить в корзину (сессия):**
```python
def add_to_cart(request, game_id):
    cart = request.session.get('cart', {})
    game_id_str = str(game_id)
    cart[game_id_str] = cart.get(game_id_str, 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', 'index'))
```

→ Корзина хранится в браузер-сессии. Работает **без регистрации**.

---

**Поиск, фильтр, сортировка:**
```python
def game_list_by_genre(request, slug):
    qs = Game.objects.filter(genre__slug=slug)
    
    # Поиск
    q = request.GET.get("q", "")
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
    
    # Цена
    if request.GET.get("min_price"):
        qs = qs.filter(price__gte=request.GET["min_price"])
    
    # Сортировка
    sort = request.GET.get("sort", "name")
    qs = qs.order_by(sort)
    
    # Пагинация
    page_obj = Paginator(qs, 8).get_page(request.GET.get("page"))
    return render(request, "game_list.html", {"page_obj": page_obj})
```

→ Фильтруем по жанру, ищем, сортируем, делим на страницы.

---

**Оформление заказа:**
```python
def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        
        # Создаем заказ
        order = Order.objects.create(
            full_name=request.POST['full_name'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            status='new'
        )
        
        # Добавляем товары
        for game_id, qty in cart.items():
            OrderItem.objects.create(
                order=order,
                game_id=int(game_id),
                price=Game.objects.get(id=game_id).price
            )
        
        request.session['cart'] = {}
        return redirect('order_detail', order_id=order.id)
    
    return render(request, 'orders/checkout.html')
```

→ Берем данные из формы, создаем Order + OrderItems в БД, очищаем корзину.

---

## 🎨 HTML шаблоны

**Главная (index.html):**
```html
<div class="grid">
  {% for game in games %}
    <div class="game-card">
      <img src="{{ game.images.first.image.url }}" alt="{{ game.name }}">
      <h3>{{ game.name }}</h3>
      <p>${{ game.price }}</p>
      <a href="{% url 'add_to_cart' game.id %}" class="btn">Add to Cart</a>
    </div>
  {% endfor %}
</div>
```

**Детали игры (game_detail.html):**
```html
<div class="game-detail">
  <img src="{{ game.images.first.image.url }}" class="main-image">
  <h1>{{ game.name }}</h1>
  <p>${{ game.price }}</p>
  <p>{{ game.description }}</p>
  <a href="{% url 'add_to_cart' game.id %}" class="btn">Add to Cart</a>
</div>
```

**Корзина (cart.html):**
```html
<table>
  {% for item in games %}
    <tr>
      <td>{{ item.game.name }}</td>
      <td>${{ item.game.price }}</td>
      <td>{{ item.quantity }}</td>
      <td>${{ item.subtotal }}</td>
    </tr>
  {% endfor %}
</table>
<p><strong>Total: ${{ total_sum }}</strong></p>
<a href="{% url 'checkout' %}" class="btn">Checkout</a>
```

**Оформление (checkout.html):**
```html
<form method="POST">
  {% csrf_token %}
  <input type="text" name="full_name" placeholder="Full Name" required>
  <input type="text" name="phone" placeholder="Phone" required>
  <input type="text" name="address" placeholder="Address" required>
  <button type="submit">Create Order</button>
</form>
```

---

## 5️⃣ CSS (адаптивный дизайн)

```css
/* Сетка для карточек */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

/* Карточка игры */
.game-card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
}

.game-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

/* Изображение в карточке */
.game-card-image-wrapper {
  width: 100%;
  height: 220px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
}

.game-card-image-wrapper img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;  /* Не обрезаются, видно целиком */
}

/* Детали игры */
.game-detail-card > div {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}

/* Адаптивность под мобилку */
@media (max-width: 768px) {
  .grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }

  .game-detail-card > div {
    grid-template-columns: 1fr;  /* Одна колонна вместо двух */
  }
}
```

**Объяснение:**
- Grid для расположения карточек (автоматически масштабируется)
- `object-fit: contain` — изображения не обрезаются
- `@media` — правила для мобильных (одна колонна вместо двух)

---

## 6️⃣ URL маршруты

```python
# config/urls.py
urlpatterns = [
    path('', views.index, name='index'),
    path('genres/', views.genre_list, name='genre_list'),
    path('genre/<slug:slug>/', views.game_list_by_genre, name='game_list_by_genre'),
    path('game/<slug:slug>/', views.game_detail, name='game_detail'),
    
    path('cart/', views.view_cart, name='cart'),
    path('add-to-cart/<int:game_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:game_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
]
```

**Объяснение:** Маршруты для всех страниц (главная, жанры, игры, корзина, заказ).

---

## 7️⃣ Жизненный цикл покупки

```
1. Пользователь → index() → видит 10 новых игр
   
2. Нажимает на жанр → game_list_by_genre() → фильтруем по жанру
   
3. Ищет игру → request.GET.get('q') → Q(name__icontains=q)
   
4. Нажимает на игру → game_detail() → видим описание и скриншоты
   
5. "Add to Cart" → add_to_cart() → сохраняем в request.session['cart']
   
6. Открывает корзину → view_cart() → показываем товары из session
   
7. "Checkout" → form ФИ, телефон, адрес
   
8. Отправляет → Order.objects.create() → создаем заказ в БД
   
9. Показываем подтверждение → redirect('order_detail')
```

---

## 🎯 Ключевые код-паттерны

| Что | Как |
|-----|-----|
| **Поиск** | `Q(name__icontains=q) \| Q(desc__icontains=q)` |
| **Фильтр цены** | `filter(price__gte=min, price__lte=max)` |
| **Сортировка** | `order_by('price')` или `order_by('-price')` |
| **Пагинация** | `Paginator(qs, 8).get_page(page_num)` |
| **Корзина** | `request.session['cart'] = {game_id: qty}` |
| **Заказ** | `Order.objects.create(...) + OrderItem.objects.create(...)` |
| **Картинки** | `object-fit: contain` — видно целиком |
| **Адаптив** | `@media (max-width: 768px)` — для мобилок |

---

## 📊 Результат

✅ 3 Django приложения (catalog, orders, accounts)  
✅ 6 моделей в БД  
✅ Поиск + фильтрация + сортировка  
✅ Сессионная корзина (без регистрации)  
✅ Заказы в БД с позициями  
✅ Адаптивный HTML + CSS  
✅ Правильная обработка картинок  
✅ Полностью на Django  

---

**April 3, 2026 | Готово к защите 🎓**
