
from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
   list_display = (
      "id",
      "product",
      "low_stock_threshold",
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
