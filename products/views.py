from django.views.generic import ListView, DetailView
from .models import Product

class ProductListview(ListView):
   model = Product
   template_name = "products/product_list.html"
   context_object_name = "products"

   def get_queryset(self):
      return Product.objects.filter(
         is_active=True
      )

"""
1. What is ListView?
= ListView is a Django generic class-based view used to display a list of objects from a model.
2. What does get_queryset() do>
= get_queryset() allows us to customize which objects are returned by a class-based view.
3. Why use context_object_name?
= It allows us to define a meaningful name for the objects passed to the template.
4. What is a QuerySet?
= A QuerySet is a collection of database queries representing objects retrieved from a Django model.

"""

class ProductDetailView(DetailView):
   model = Product
   template_name = "products/product_detail.html"
   context_object_name = "product"

   def get_queryset(self):
      return Product.objects.filter(
         is_active=True
      )


"""

1. What is Django DetailView?
= DetailView is a Django generic class-based view used to display the details of a single model object.
2. What is pk?
= pk stands for Primary Key. It is used to uniquely identify a database record.
3. What does <int:pk> meand?
= It captures an integer value from the URL and passes it to the view as pk.
Example:
   /products/10/
   pk = 10

"""

