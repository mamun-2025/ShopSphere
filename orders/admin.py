

from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
   model = OrderItem
   extra = 0
   can_delete = False
   readonly_fields = (
      "product",
      "product_name",
      "unit_price",
      "quantity",
      "is_taxable",
      "tax_rate",
      "tax_amount",
      "lien_total",

   )



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
   list_display = (
      "order_number",
      "user",
      "status",
      "payment_method",
      "payment_status",
      "total",
      "created_at",
   )

   list_filter = (
      "status",
      "payment_method",
      "payment_status",
      "created_at",
   )

   search_fields = (
      "order_number",
      "user__username",
      "user__email",
      "shipping_phone",
   )

   readonly_fields = (
      "order_number",
      "user",
      "payment_method",
      "payment_status",
      "shipping_full_name",
      "shipping_phone",
      "shipping_address_line",
      "shipping_area",
      "shipping_city_or_district",
      "shipping_postal_code",
      "shipping_instructions",
      "estimated_delivery_days",
      "subtotal",
      "tax_amount",
      "shipping_fee",
      "total",
      "created_at",
      "updated_at",

   )

   inlines = [OrderItemInline]

   