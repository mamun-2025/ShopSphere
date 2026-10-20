

from django.urls import path 

from . import views

app_name = "wishlist"

urlpatterns = [
    path(
       "add/<int:product_id>/",
       views.AddToWishlistView.as_view(),
       name="add",
    ),
]
