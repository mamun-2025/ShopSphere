
from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

   list_display = (
      "id",
      "user",
      "created_at",
      "updated_at",
   )

   search_fields = (
      "user__username",
      "user__email",
   )

   readonly_fields = (
      "created_at",
      "updated_at",
   )

   list_select_related = (
      "user",
   )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
   list_display = (
      "id",
      "cart",
      "product",
      "quantity",
      "created_at",
   )

   search_fields = (
      "cart__user__username",
      "cart__user__email",
      "product__name",
      "product__sku",
   )

   list_select_related = (
      "cart",
      "product",
   )

   readonly_fields = (
      "created_at",
   )