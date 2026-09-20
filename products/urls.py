

from django.urls import path
from .views import (
   ProductListview,
   ProductDetailView,
   ProductCreateView,
   ProductUpdateView
)

urlpatterns = [
   
   path("", 
         ProductListview.as_view(),
         name="product_list",
      ),
   path("create/",
           ProductCreateView.as_view(),
           name="product_create",
      ),
   path("<int:pk>/update/",
           ProductUpdateView.as_view(),
           name="product_update",
      ),
   path("<int:pk>/",
        ProductDetailView.as_view(),
        name="product_detail",
      ),
  
]
