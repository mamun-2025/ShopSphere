
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.urls import reverse

from products.models import Product

from .forms import ReviewForm
from .models import Review


# Review CreateView
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

      if Review.objects.filter(
         user=self.request.user,
         product=self.product,
      ).exists():

         form.add_error(
            None,
            "You have already reviewed this porduct."
         )

         return self.form_invalid(form)

      try:

         with transaction.atomic():

            response = super().form_valid(form)

      except IntegrityError:

         form.add_error(
            None,
            "You have already reviewed this product."
         )

      return response



   def get_success_url(self):
      
      return reverse(
         "product_detail",
         kwargs={
            "slug": self.product.slug,
         },
      )



# Review UpdateView
class ReviewUpdateView(LoginRequiredMixin, UpdateView):

   model = Review

   form_class = ReviewForm

   template_name = "reviews/review_form.html"

   pk_url_kwarg = "review_id"

   def get_object(self, queryset=None):

      return get_object_or_404(
         Review,
         pk = self.kwargs["review_id"],
         user = self.request.user,
      )

   def get_success_url(self):

      return reverse(
         "product_detail",
         kwargs={
            "slug": self.object.product.slug,
         },
      )