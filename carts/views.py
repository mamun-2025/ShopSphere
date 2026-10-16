
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views import View

from products.models import Product
from .models import Cart, CartItem

from django.views.generic import FormView
from .forms import CartQuantityForm



# Add to Cart
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
            "products:product_detail",
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
               "products:product_detail",
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
            quantity=1,
         )


      messages.success(
         request,
         f"{product.name} added to cart.",
      )

      return redirect(
         "products:product_detail",
         slug=product.slug,
      )

         


# Update Cart Quantity
class UpdateCartQuantityView(
   LoginRequiredMixin,
   FormView,
):
   template_name = "carts/update_quantity.html"
   form_class = CartQuantityForm

   def dispatch(self, request, *args, **kwargs):

      self.cart_item = get_object_or_404(
         CartItem.objects.select_related(
            "cart",
            "product",
         ),
         pk=kwargs["item_id"],
         cart__user=request.user,
      )

      return super().dispatch(
         request, 
         *args,
         **kwargs
      )


   def get_initial(self):

      return {
         "quantity": self.cart_item.quantity,
      }


   def form_valid(self, form):

      quantity = form.cleaned_data["quantity"]

      if quantity > self.cart_item.product.stock:
          
         form.add_error(
             "quantity",
             "Requested quantity exceeds available stock.",
          )

         return self.form_invalid(form)

      self.cart_item.quantity = quantity

      self.cart_item.save(
         update_fields=["quantity"],
      )

      messages.success(
         self.request,
         "Cart quantity updated successfully.",
      )

      return redirect(
         "products:product_detail",
         slug=self.cart_item.product.slug,
      )

      # return redirect(
      #    "carts:detail",
      # )
   

      
# Remove Cart 
class RemoveFromCartView(
   LoginRequiredMixin,
   View,
):
   def post(self, request, item_id):

      cart_item = get_object_or_404(
         CartItem.objects.select_related("product"),
         pk=item_id,
         cart__user=request.user,
      )

      product = cart_item.product
      product_name = product.name 

      cart_item.delete()

      messages.success(
         request,
         f"{product_name} removed from cart.",
      )

      return redirect(
         "products:product_detail",
         slug=product.slug,
      )


   

