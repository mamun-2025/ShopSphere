
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse

from products.models import Product

from .forms import ReviewForm
from .models import Review

class ReviewCreateView(LoginRequiredMixin, CreateView):
   model = Review
   form_class = ReviewForm
   template_name = "reviews/review_form.html"

   def dispatch(self, request, *args, **kwargs):

      self.product = get_object_or_404(
         Product,
         pk=kwargs["product_id"],
         is_active=True,
         
      )
      return super().dispatch(
         request, 
         *args, 
         **kwargs,
      )


   def form_valid(self, form):

      form.instance.user = self.request.user 

      form.instance.product = self.product

      response = super().form_valid(form)

      return response


   def get_success_url(self):
      
      return reverse(
         "product_detail",
         kwargs={
            "slug": self.product.slug,
         },
      )


   