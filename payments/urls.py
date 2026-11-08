

from django.urls import path 

from payments import views

app_name = "payments"


urlpatterns = [
    path(
       "sslcommerz/start/<int:order_id>/",
       views.sslcommerz_payment_start,
       name="sslcommerz_start",
    ),
    path(
       "sslcommerz/success/",
       views.sslcommerz_success,
       name="sslcommerz_success",
    ),
    path(
       "sslcommerz/fail/",
       views.sslcommerz_fail,
       name="sslcommerz_fail",
    ),
    path(
       "sslcommerz/cancel/",
       views.sslcommerz_cancel,
       name="sslcommerz_cancel",
    ),
   
    
]
