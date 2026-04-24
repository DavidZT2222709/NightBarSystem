# apps/tables/admin.py
from django.contrib import admin
from .models import Table

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('numero', 'capacidad', 'estado')
    list_filter = ('estado',)
    list_editable = ('estado',) # Para liberar mesas rápido desde el PC
    search_fields = ('numero',)