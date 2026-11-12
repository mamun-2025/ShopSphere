
from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
   list_display = (
      "code",
      "discount_type",
      "discount_value",
      "minimum_order_amount",
      "maximum_discount",
      "start_at",
      "end_at",
      "used_count",
      "usage_limit",
      "is_active",
   )

   list_filter = (
      "discount_type",
      "is_active",
      "start_at",
      "end_at",
   )

   search_fields = (
      "code",
   )

   readonly_fields = (
      "created_at",
      "updated_at",
      "used_count",
   )

   ordering = (
      "-created_at",
   )

   date_hierarchy = "created_at"

   list_per_page = 20

   fieldsets = (
      ( 
         "Coupon Information",
         {
            "fields":(
               "code",
               "is_active",
            )
         },
      ),
      (
         "Discount Configuration",
         {
            "fields":(
               "discount_type",
               "discount_value",
               "minimum_order_amount",
               "maximum_discount",
            )
         },
      ),
      (
         "Coupon Validity",
         {
            "fields":(
               "start_at",
               "end_at",
            )
         },
      ),
      (
         "Usage Configuration",
         {
            "fields":(
               "usage_limit",
               "used_count",
               "per_user_limit",
            )
         },
      ),
      (
         "Timestamps",
         {
            "fields":(
               "created_at",
               "updated_at",
            ),
            "classes":("collapse",),
         },
      ),
   )