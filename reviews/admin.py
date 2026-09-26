
from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
   list_display = (
      "id",
      "user",
      "product",
      "rating",
      "is_active",
      "created_at",
      "updated_at",
   )

   list_filter = (
      "rating",
      "is_active",
      "created_at",
   )

   search_fields = (
      "user__username",
      "product__name",
      "comment",
   )

   readonly_fields = (
      "created_at",
      "updated_at",
   )



