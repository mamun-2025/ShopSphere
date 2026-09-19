

from django.urls import path
from .views import (
   ProductListview,
   ProductDetailView,

)

urlpatterns = [
   path("", 
         ProductListview.as_view(),
         name="product_list",
      ),
   path("<int:pk>/",
        ProductDetailView.as_view(),
        name="product_detail",
      ),
]
