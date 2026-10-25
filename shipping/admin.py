
from django.contrib import admin
from .models import ShippingMethod, ShippingAddress


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
   list_display = (
      "name",
      "cost",
      "free_shipping_threshold",
      "estimated_delivery_days",
      "is_active",
   )

   list_filter = (
      "is_active",
   )

   search_fields = (
      "name",
      "description",
   )

   readonly_fields = (
      "created_at",
      "updated_at",
   )



@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
   list_display = (
      "user",
      "full_name",
      "phone",
      "city_or_district",
      "is_default",
   )

   list_filter = (
      "is_default",
      "city_or_district",
   )

   search_fields = (
      "full_name",
      "phone",
      "user__username",
      "city_or_district",
      "area",
   )

   readonly_fields = (
      "created_at",
      "updated_at",
   )

   