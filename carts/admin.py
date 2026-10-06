
from django.contrib import admin
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

   list_display = (
      "id",
      "user",
      "created_at",
      "updated_at",
   )

   search_fields = (
      "user__username",
      "user__email",
   )

   readonly_fields = (
      "created_at",
      "updated_at",
   )

   list_select_related = (
      "user",
   )
