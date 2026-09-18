from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
   list_display = (
      "id",
      "name",
      "category",
      "sku",
      "price",
      "stock",
      "is_active",
      "created_at",
   )

   list_filter = (
      "category",
      "is_active",
      "created_at",
   )

   search_fields = (
      "name",
      "description",
      "sku",
   )

   ordering = (
      "-created_at",
   )