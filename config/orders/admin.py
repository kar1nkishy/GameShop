from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'status', 'created_at')
    list_editable = ('status',)  # Позволяет менять статус прямо в списке
    list_filter = ('status', 'created_at')  # Фильтр по статусу и дате
    search_fields = ('full_name', 'phone', 'id')  # Поиск по имени, телефону, ID
    readonly_fields = ('created_at', 'id')  # Защита от изменения даты и ID
    fields = ('id', 'user', 'full_name', 'phone', 'address', 'status', 'created_at')  # Порядок полей при редактировании
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'game', 'price')