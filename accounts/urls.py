

from django.urls import path 
from . import views 
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
   # Authentication
   path("register/", views.register, name="register"),
   path("login/", views.user_login, name="login"),
   path("logout/", views.user_logout, name="logout"),

   # Customer Profile
   path("profile/", views.profile, name="profile"),
   path("profile/edit/", views.edit_profile, name="edit_profile"),
   path("password/change/", views.change_password, name="change_password"),

   # Password Reset 
   path(
      "password-reset/",
      auth_views.PasswordResetView.as_view(
         template_name="accounts/password_reset.html"
      ),
      name="password_reset",
   ),
   path(
      "password-reset/done/",
      auth_views.PasswordResetDoneView.as_view(
         template_name="accounts/password_reset_done.html"
      ),
      name="password_reset_done",
   ),
   path(
      "reset/<uidb64>/<token>/",
      auth_views.PasswordResetConfirmView.as_view(
         template_name="accounts/password_reset_confirm.html"
      ),
      name="password_reset_confirm",
   ),
   path(
      "reset/done/",
      auth_views.PasswordResetCompleteView.as_view(
         template_name="accounts/password_reset_complete.html"
      ),
      name="password_reset_complete",
   ),

   # Admin Customer Management
   path(
      "admin/customers/",
      views.AdminCustomerListView.as_view(),
      name="admin_customer_list",
   ),
   path(
      "admin/customers/<int:pk>/",
      views.AdminCustomerDetailView.as_view(),
      name="admin_customer_detail",
   )





]

