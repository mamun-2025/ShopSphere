
from django.urls import path 

from .views import CheckoutView, OrderDetailView

app_name = "orders"

urlpatterns = [
    path(
       "checkout/",
       CheckoutView.as_view(),
       name="checkout",
    ),
    path(
       "<uuid:order_number/",
       OrderDetailView.as_view(),
       name="detail",
    ),
    
]
