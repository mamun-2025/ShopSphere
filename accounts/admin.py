from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
   list_display = (
      "id",
      "username",
      "email",
      "phone",
      "is_staff",
      "is_active",
      "date_joined",
   )

   list_display_links = (
      "id",
      "username",
   )

   list_filter = (
      "username",
      "email",
      "phone",
   )

   ordering = (
      "-date_joined",
   )

   readonly_fields = (
      "last_login",
      "date_joined",
   )

   list_per_page = 20

   date_hierarchy = "date_joined"

   save_on_top = True

   filter_horizontal = (
      "groups",
      "user_permissions",
   )

   empty_value_diplay= "-"

   fieldsets = (
      (
         "Account_Information",{
            "fields":(
               "username",
               "password",
            )

         }),

      (
         "Personal_Information",{
            "fields":(
               "firstname",
               "lastname",
               "email",
               "phone",
               "profile_picture",
               "date_of_birth",
               "address",
            )
         }),

      (
         "Permissions",{
            "fields":(
               "is_staff",
               "is_active",
               "is_superuser",
               "groups",
               "user_permissions",
            )
         }),

      (
         "Important_dates",{
            "fields":(
               "last_login",
               "date_joined",
            )
         }),
   )

   add_fieldsets = (
      (
         None,
         {
            "classes": ("wide",),
            "fields":(
               "username",
               "email",
               "phone",
               "password1",
               "password2",
               "is_staff",
               "is_active",
            ),
         },
      ),
   )
   
   
   
