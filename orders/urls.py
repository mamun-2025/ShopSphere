
from django.urls import path 

from .views import (
   CheckoutView, 
   OrderDetailView, 
   BuyNowView, 
   OrderHistoryView,
   OrderCancelView,
   AdminOrderDashboardView,
   AdminOrderListView,
   AdminOrderDetailView,
   AdminOrderStatusUpdateView,
)

app_name = "orders"

urlpatterns = [
    path(
      "admin/",
      AdminOrderDashboardView.as_view(),
      name="admin_dashboard",
       ),
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
       "history/",
       OrderHistoryView.as_view(),
       name="history",
    ),
    path(
       "<uuid:order_number>/cancel/",
       OrderCancelView.as_view(),
       name="cancel",
    ),
    path(
       "<uuid:order_number>/",
       OrderDetailView.as_view(),
       name="detail",
    ),
    path(
       "admin/orders/",
       AdminOrderListView.as_view(),
       name="admin_order_list",
    ),
    path(
       "admin/orders/<uuid:order_number>/",
       AdminOrderDetailView.as_view(),
       name="admin_order_detail",
    ),
    path(
       "admin/orders/<uuid:order_number>/status/",
       AdminOrderStatusUpdateView.as_view(),
       name="admin_order_status_update",
    ),

    
]
