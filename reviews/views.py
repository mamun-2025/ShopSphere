
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib import messages

from products.models import Product

from .forms import ReviewForm
from .models import Review


# Review CreateView
class ReviewCreateView(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
   model = Review
   form_class = ReviewForm
   template_name = "reviews/review_form.html"
   permission_required = "reviews.add_review"

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
            "You have already reviewed this product."
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

         return self.form_invalid(form)

      messages.success(
         self.request,
         "Your review has been successfully sumitted.",
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
class ReviewUpdateView(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):

   model = Review

   form_class = ReviewForm

   template_name = "reviews/review_form.html"

   pk_url_kwarg = "review_id"

   permission_required = "reviews.change_review"


   def get_queryset(self):

      return Review.objects.filter(
         user=self.request.user
      )

   def get_success_url(self):

      return reverse(
         "product_detail",
         kwargs={
            "slug": self.object.product.slug,
         },
      )

   def form_valid(self, form):

      messages.success(
         self.request,
         "Your review has been updated successfully.",
      )

      return super().form_valid(form)

   



# Review DeleteView
class ReviewDeleteView(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):

   model = Review

   template_name = "reviews/review_confirm_delete.html"

   pk_url_kwarg = "review_id"

   permission_required = "reviews.delete_review"
   

   def get_queryset(self):

      return Review.objects.filter(
         user=self.request.user
      )

   def get_success_url(self):
      
      return reverse(
         "product_detail",
         kwargs={
            "slug": self.object.product.slug,
         },
      )

   def form_valid(self, form):

      messages.success(
         self.request,
         "Your review has been deleted successfully.",
      )

      return super().form_valid(form)
   
   