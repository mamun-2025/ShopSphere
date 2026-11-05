from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PayemntAdmin(admin.ModelAdmin):
   list_display = (
      "payment_reference",
      "order",
      "user",
      "amount",
      "currency",
      "method",
      "status",
      "geteway_transaction_id",
      "created_at",
   )

   search_fields = (
      "payment_reference",
      "gateway_transaction_id",
      "order__id",
      "user__username",
      "user__email",
   )

   list_filter = (
      "status",
      "method",
      "currency",
      "created_at",
   )

   date_hierarchy = "created_at"

   list_select_related = (
      "order",
      "user",
   )

   list_per_page = 25

   ordering = ("-created_at")

   fieldsets = (
      (
         "Payment Identification",
         {
            "fields": (
               "payment_reference",
               "order",
               "user",
            )
         },
      ),
      (
         "Payment Information",
         {
            "fields": (
               "amount",
               "currency",
               "method",
               "status",
            )
         },
      ),
      (
         "Gateway Information",
         {
            "fields": (
               "gateway_transaction_id",
            )
         },
      ),
      (
         "Timestamps",
         {
            "fields": (
               "created_at",
               "updated_at",
            )
         },
      ),
   )

   readonly_fields = (
      "payment_reference",
      "order",
      "user",
      "amount",
      "currency",
      "method",
      "status",
      "gateway_traction_id",
      "created_at",
      "updated_at",
   )

   def has_add_permission(self, request):
      return False

   def has_delete_permission(self, request, obj=None):
      return False
   