from django.contrib import admin

from .models import Product, Stock, StockProduct

class RelationshipInline(admin.TabularInline):
    model = StockProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_filter = ['address']

@admin.register(StockProduct)
class StockProductAdmin(admin.ModelAdmin):
    list_filter = ['price']
