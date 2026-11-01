
from django.urls import path 

from .views import CheckoutView, OrderDetailView, BuyNowView

app_name = "orders"

urlpatterns = [
    path(
       "checkout/",
       CheckoutView.as_view(),
       name="checkout",
    ),
    path(
       "buy-now/<int:product_id>/",
       BuyNowView.as_view(),
       name="buy_now",
    ),
    path(
       "<uuid:order_number>/",
       OrderDetailView.as_view(),
       name="detail",
    ),
    
]
