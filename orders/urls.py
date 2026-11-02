
from django.urls import path 

from .views import CheckoutView, OrderDetailView, BuyNowView, OrderHistoryView

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
    path(
       "history/",
       OrderHistoryView.as_view(),
       name="history"
    ),
    
]
