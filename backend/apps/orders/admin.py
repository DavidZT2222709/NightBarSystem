from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model  = OrderItem
    extra  = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ['id', 'mesero', 'table', 'status', 'created_at']
    list_filter   = ['status']
    ordering      = ['created_at']
    inlines       = [OrderItemInline]  # Muestra los items dentro del pedido

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']