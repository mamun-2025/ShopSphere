from django.contrib import admin

from .models import TaxRate



@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
   list_display = (
      "name",
      "rate",
      "is_active",
      "is_default",
      "updated_at",
   )

   list_filter = (
      "is_active",
      "is_default",
   )

   search_fields = (
      "name",
   )

   list_editable = (
      "rate",
      "is_active",
      "is_default",
   )

   readonly_fields = (
      "created_at",
      "updated_at",
   )
