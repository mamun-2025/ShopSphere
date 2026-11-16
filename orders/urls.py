
from django.urls import path 

from .views import (
   CheckoutView, 
   OrderDetailView, 
   BuyNowView, 
   OrderHistoryView,

   CustomerOrderCancellationRequestView,

   AdminOrderDashboardView,
   AdminOrderListView,
   AdminOrderDetailView,
   AdminOrderStatusUpdateView,

   AdminCancellationListView,
   AdminApproveCancellationView,
   AdminRejectCancellationView,
   AdminDirectCancellationView,
)

app_name = "orders"

urlpatterns = [

   # Admin Dashboard
    path(
      "admin/",
      AdminOrderDashboardView.as_view(),
      name="admin_dashboard",
       ),

   # Customer
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

   # Customer Cancellation Request
    path(
       "<uuid:order_number>/cancel/",
       CustomerOrderCancellationRequestView.as_view(),
       name="cancel",
    ),

   # Order Detail
    path(
       "<uuid:order_number>/",
       OrderDetailView.as_view(),
       name="detail",
    ),



   # Admin Order management
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



   # Admin Cancellation Management
    path(
       "admin/cancellations/",
       AdminCancellationListView.as_view(),
       name="admin-cancellation-list",
    ),

    path(
       "admin/cancellations/<int:cancellation_id>/approve/",
       AdminApproveCancellationView.as_view(),
       name="admin-approve-cancellation",
    ),

    path(
       "admin/cancellations/<int:cancellation_id>/reject/",
       AdminRejectCancellationView.as_view(),
       name="admin-reject-cancellation",
    ),

   # Direct Admin Cancellation
   path(
      "admin/orders/<uuid:order_number>/cancel/",
      AdminDirectCancellationView.as_view(),
      name="admin-direct-cancellation",
   ),
    
]
