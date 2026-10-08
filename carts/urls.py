

from django.urls import path 
from . import views

app_name = "carts"

urlpatterns = [
    path(
       "add/<int:product_id>/",
       views.AddToCartView.as_view(),
       name="add",
    ),
    
]
