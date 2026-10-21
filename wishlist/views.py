
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from products.models import Product
from .models import WishlistItem


# Add To WishlistView
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



# WishlistListView
class WishlistListView(LoginRequiredMixin, ListView):
   model = WishlistItem
   template_name = "wishlist/wishlist_list.html"
   context_object_name = "wishlist_items"

   def get_queryset(self):
      return (
         WishlistItem.objects.filter(
            user=self.request.user 
         ).select_related("product")
      )



# RemoveFromWishListView
class RemoveFromWishlistView(LoginRequiredMixin, View):
   def post(self, request, item_id):
      item = get_object_or_404(
         WishlistItem,
         pk=item_id,
         user=request.user,
      )

      product_name = item.product.name 
      item.delete()

      messages.success(
         request,
         f"{product_name} removed your wishlist.",
      )

      return redirect(
         "wishlist:list",
      )
   