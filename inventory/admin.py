
from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
   list_display = (
      "id",
      "product",
      "current_stock",
      "low_stock_threshold",
      "low_stock_display_status",
      "created_at",
      "updated_at",
   )

   search_fields = (
      "product__name",
      "product__sku",
   )

   readonly_fields = (
      "created_at",
      "updated_at",
   )

   @admin.display(
      description="Current Stock",
   )

   def current_stock(self, obj):
      return obj.product.stock 


   @admin.display(
      boolean=True,
      description="Low Stock",
   )

   def low_stock_display_status(self, obj):
      return obj.is_low_stock


