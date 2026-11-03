
from django import forms
from django.contrib import admin

from .models import Order, OrderItem
from .services import (
   ALLOWED_STATUS_TRANSITIONS,
   update_order_status,
)


class OrderAdminForm(forms.ModelForm):
   class Meta:
      model = Order
      fields = "__all__"

   def clean_status(self):
      new_status = self.cleaned_data["status"]

      if not self.instance.pk:
         return new_status

      try:
         old_order = Order.objects.only("status").get(
            pk=self.instance.pk
         )
      except Order.DoesNotExist:
         raise forms.ValidationError(
            "This order no longer exists."
         )

      old_status = old_order.status

      if new_status == old_status:
         return new_status

      allowed_statuses = ALLOWED_STATUS_TRANSITIONS.get(
         old_status,
         set(),
      )

      if new_status not in allowed_statuses:
         raise forms.ValidationError(
            f"Cannot change status from"
            f"{old_order.get_status_display()} "
            f"to {self.instance.get_status_display()}."
         )

      return new_status



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
      "line_total",
   )



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

   form = OrderAdminForm

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
      "shipping_zone_name",
      "shipping_method_name",
      "estimated_delivery_days",
      "subtotal",
      "tax_amount",
      "shipping_fee",
      "service_fee",
      "total",
      "created_at",
      "updated_at",

   )

   inlines = [OrderItemInline]

   def save_model(self, request, obj, form, change):

      if change:
         old_order = Order.objects.only("status").get(
            pk=obj.pk
         )

         if old_order.status != obj.status:
            updated_order = update_order_status(
               order_id=obj.pk,
               new_status=obj.status,
            )

            obj.status = updated_order.status

      
      super().save_model(
         request, 
         obj, 
         form, 
         change
      )

   