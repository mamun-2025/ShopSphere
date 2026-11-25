

from django.contrib import messages
from django.contrib.auth.mixins import (
   LoginRequiredMixin,
   PermissionRequiredMixin,
)
from django.db.models import Q, Avg, Count
from django.urls import reverse_lazy
from django.views.generic import (
   ListView,
   DetailView,
   CreateView,
   UpdateView,
   DeleteView,
)

from .models import Product
from .forms import ProductForm


### Product ListView
class ProductListView(ListView):
   model = Product
   template_name = "products/product_list.html"
   context_object_name = "products"
   paginate_by = 5

   def get_queryset(self):
      queryset = (
         Product.objects
         .filter(
            is_active=True,
            category__is_active=True,
         )
         .select_related("category")
      )

      search_query = self.request.GET.get("search", "").strip()

      if search_query:
         queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(description__icontains=search_query)
         )

      return queryset



### Product DetailView
class ProductDetailView(DetailView):
   model = Product
   template_name = "products/product_detail.html"
   context_object_name = "product"
   slug_field = "slug"

   def get_queryset(self):

      return (Product.objects
         .filter(
            is_active=True,
            category__is_active=True
         )
         .select_related("category")
         .annotate(
            average_rating=Avg(
               "reviews__rating",
               filter=Q(
                  reviews__is_active=True
               ),
            ),
            total_reviews=Count(
               "reviews",
               filter=Q(
                  reviews__is_active=True
               ),
            ),
         )
      )

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)

      context["active_reviews"] = (
         self.object.reviews
         .filter(is_active=True)
         .select_related("user")
      )

      context["gallery_images"] = (
         self.object.images
         .exclude(image="")
         .exclude(image__isnull=True)
      )

      return context
   



### Product CreateView
class ProductCreateView(LoginRequiredMixin,  PermissionRequiredMixin, CreateView):
   model = Product
   form_class = ProductForm
   template_name = "products/product_form.html"
   success_url = reverse_lazy("products:product_list")
   permission_required = "products.add_product"
   raise_exception = True
   

   def form_valid(self, form):
      response = super().form_valid(form)

      messages.success(
         self.request,
         "Product create successfully"
      )

      return response



### Product UpdateView
class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
   model = Product
   form_class = ProductForm
   template_name = "products/product_form.html"
   context_object_name = "product"
   success_url = reverse_lazy("products:product_list")
   permission_required = "products.change_product"
   raise_exception = True


   def form_valid(self, form):
      response = super().form_valid(form)

      messages.success(
         self.request,
         "Product updated successfully"
      )

      return response




### Product DeleteView
class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
   model = Product
   template_name = "products/product_confirm_delete.html"
   context_object_name = "product"
   success_url = reverse_lazy("products:product_list")
   permission_required = "products.delete_product"
   raise_exception = True

   def form_valid(self, form):
      response = super().form_valid(form)

      messages.success(
         self.request,
         "Product deleted succssfully",
      )

      return response


