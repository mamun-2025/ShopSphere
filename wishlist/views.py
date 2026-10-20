
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from products.models import Product
from .models import WishlistItem

class AddToWishlistView(LoginRequiredMixin, View):
   def post(self, request, product_id):
      product = get_object_or_404(
         Product,
         pk=product_id,
      )

      item, created = WishlistItem.objects.get_or_create(
         user=request.user,
         product=product,
      )

      if created:
         messages.success(
            request,
            f"{product.name} added to your wishlist."
         )

      else:
         messages.info(
            request,
            f"{product.name} is already in your wishlist."
         )

      return redirect(
         "products:product_detail",
         slug=product.slug,
      )
