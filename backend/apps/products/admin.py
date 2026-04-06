from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name', 'price', 'available']
    list_filter   = ['available']
    search_fields = ['name']