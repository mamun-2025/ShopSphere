

from django.urls import path 

from . import views

app_name = "wishlist"

urlpatterns = [
    path("", views.WishlistListView.as_view(), name="list"),
    path(
       "add/<int:product_id>/",
       views.AddToWishlistView.as_view(),
       name="add",
    ),
    path(
       "item/<int:item_id>/remove/",
       views.RemoveFromWishlistView.as_view(),
       name="remove",
    ),
]
