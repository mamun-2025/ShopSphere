from django.contrib import admin
from .models import Product, ProductImage

# Product Admin
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


# ProductImage Admin 
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
   list_display = (
      "id",
      "product",
      "alt_text",
      "created_at",
   )