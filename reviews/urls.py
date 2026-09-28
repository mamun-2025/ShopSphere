

from django.urls import path 
from .views import ReviewCreateView, ReviewUpdateView

app_name = "reviews"

urlpatterns = [
   path(
      "product/<int:product_id>/create/",
      ReviewCreateView.as_view(),
      name="review_create",
   ),
   path(
      "<int:review_id>/edit/",
      ReviewUpdateView.as_view(),
      name="review_update",
   ),
   
]
