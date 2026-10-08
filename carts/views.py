
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views import View

from products.models import Product
from .models import Cart, CartItem


class AddToCartView(
   LoginRequiredMixin,
   View,
):
   def post(self, request, product_id):

      product = get_object_or_404(
         Product,
         pk=product_id,
         is_active=True,
      )

      if product.stock < 1:
         messages.error(
            request,
            "Product is out of stock."
         )
         return redirect(
            "products:detail",
            slug=product.slug,
         )

      cart, created = Cart.objects.get_or_create(
         user=request.user,
      )

      cart_item = CartItem.objects.filter(
         cart=cart,
         product=product,
      ).first()

      if cart_item:

         new_quantity = cart_item.quantity + 1

         if new_quantity > product.stock:
            messages.error(
               request,
               "Insufficient Stock.",
            )
            return redirect(
               "products:detail",
               slug=product.slug,
            )

         cart_item.quantity = new_quantity

         cart_item.save(
            update_fields=["quantity"],
         )

      else:
         CartItem.objects.create(
            cart=cart,
            product=product,
            quantiy=1,
         )


      messages.success(
         request,
         f"{product.name} added to cart.",
      )

      return redirect(
         "products:detail",
         slug=product.slug,
      )

         



