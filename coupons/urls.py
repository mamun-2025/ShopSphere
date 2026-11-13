

from django.urls import path

from . import views

urlpatterns = [
    path(
       "apply/",
       views.ApplyCouponView.as_view(),
       name="apply",
    ),
    path(
       "remove/",
       views.RemoveCouponView.as_view(),
       name="remove",
    ),
    
]
