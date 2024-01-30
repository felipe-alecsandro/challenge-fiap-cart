from django.contrib import admin
from cart.forms import CartForm
from .models.carts import Cart


class CartAdmin(admin.ModelAdmin):
    form = CartForm
    list_display = ('id', 'created_at', 'updated_at')
    list_per_page = 25
    

#admin.site.register(CartItems, CartItemsAdmin)
admin.site.register(Cart, CartAdmin)
