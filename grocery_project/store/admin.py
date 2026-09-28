from django.contrib import admin
from .models import Product, Cart, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)
    list_filter = ('price',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'address', 'date')
    list_filter = ('date',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
