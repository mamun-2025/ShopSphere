

from django.urls import path 
from . import views

app_name = "carts"

urlpatterns = [
    path(
       "add/<int:product_id>/",
       views.AddToCartView.as_view(),
       name="add",
    ),
    path(
       "item/<int:item_id>/update/",
       views.UpdateCartQuantityView.as_view(),
       name="update_quantity",
    ),
    path(
       "item/<int:item_id>/remove/",
       views.RemoveFromCartView.as_view(),
       name="remove",
    ),
    
]
