
from decimal import Decimal
from types import SimpleNamespace

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count, Q 

from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

from products.models import Product
from carts.models import Cart
from shipping.services import calculate_shipping_for_subtotal, get_shipping_selection
from taxes.services import calculate_items_totals

from .models import Order
from .services import money
from .services import create_order_from_items, create_order_from_cart, cancel_order, update_order_status, ALLOWED_STATUS_TRANSITIONS
from coupons.services import validate_and_calculate_coupon
from payments.services import start_sslcommerz_payment
from .forms import AdminOrderStatusUpdateForm


# CheckOut View
class CheckoutView(LoginRequiredMixin, View):
   template_name = "orders/checkout.html"

   def get_checkout_source(self, request):
      return request.session.get("checkout_source", "cart")

   def get_checkout_items(self, request):
      """
      Return a unified list of items for Cart or Buy Now.
      Each item has product, quantity and line_total.
      """
      source = self.get_checkout_source(request)

      if source == "cart":
         cart = Cart.objects.filter(
            user=request.user
         ).first()

         if not cart:
            raise ValidationError(
               "Your cart does not exist."
            )

         cart_items = list(
            cart.items.select_related("product").all()
         )

         if not cart_items:
            raise ValidationError("Your cart is empty.")

         stock_issues = cart.get_stock_issues()

         if stock_issues:
            messages.error(
               request,
               "Please resolve stock issues before checkout.",
            )

         items = []

         for item in cart_items:
            items.append(
               SimpleNamespace(
                  product=item.product,
                  quantity=item.quantity,
                  line_total=(
                     item.product.price * item.quantity
                  ),
               )
            )

         return items


      if source == "buy_now":
         product_id = request.session.get(
            "buy_now_product_id"
         )
         quantity = request.session.get(
            "buy_now_quantity"
         )

         try:
            product_id = int(product_id)
            quantity = int(quantity)
         except (TypeError, ValueError):
            raise ValidationError(
               "Your buy now session is invalid. Please try again."
            )

         if quantity < 1:
            raise ValidationError("Invalid product quantity.")

         product = Product.objects.filter(
            pk=product_id,
            is_active=True,
         ).first()

         if product is None:
            raise ValidationError(
               "The product is no longer available."
            )

         if product.stock < quantity:
            raise ValidationError(
               f"Insufficient stock for {product.name}."
               f"Available: {product.stock}."
            )

         return [
            SimpleNamespace(
               product=product,
               quantity=quantity,
               line_total=product.price * quantity,
            )
         ]

      raise ValidationError("Invalid checkout source.")


   def get(self, request):
      try:
         checkout_items = self.get_checkout_items(request)

      except ValidationError as exc:
         for error in exc.messages:
            messages.error(request, error)

         if self.get_checkout_source(request) == "buy_now":
            request.session.pop("checkout_source", None)
            request.session.pop("buy_now_product_id", None)
            request.session.pop("buy_now_quantity", None)

         return redirect("carts:detail")

      

      shipping_method, shipping_address = get_shipping_selection(
         request
      )

      if not shipping_method or not shipping_address:
         messages.info(
            request,
            "Choose a delivery address and shipping method first.",
         )
         return redirect(
            "shipping:options"
         )

      tax_summary = calculate_items_totals(checkout_items)
      shipping_summary = calculate_shipping_for_subtotal(
         subtotal=tax_summary["subtotal"],
         shipping_method=shipping_method,
         shipping_address=shipping_address,
      )

      if shipping_summary["shipping_method"] is None:
         messages.error(
            request,
            "Your shipping selection is no longer valid."
         )
         return redirect("shipping:options")

      service_fee = Decimal("0.00")
      shipping_fee = shipping_summary["shipping_fee"]


      # Coupon calculation
      coupon = None 
      discount_amount = Decimal("0.00")
      coupon_code = request.session.get("coupon_code")

      if coupon_code:
         try:
            coupon_result = validate_and_calculate_coupon(
               code=coupon_code,
               user=request.user,
               subtotal=tax_summary["subtotal"],
            )

            coupon = coupon_result["coupon"]
            discount_amount = coupon_result["discount"]

         except ValidationError as exc:

            request.session.pop("coupon_code", None)

            for error in exc.messages:
               messages.warning(request, error)


      total = (
         tax_summary["total"]
         + shipping_fee
         + service_fee
         - discount_amount
      )

      total = money(total)

      context = {
         "checkout_items": checkout_items,
         "checkout_source": self.get_checkout_source(request),

         "shipping_method": shipping_method,
         "shipping_address": shipping_address,

          **tax_summary,

         "shipping_fee": shipping_fee,
         "free_shipping": shipping_summary["free_shipping"],

         "service_fee": service_fee,

         "coupon": coupon,
         "coupon_code": coupon_code if coupon else "",
         "discount_amount": discount_amount,
         
         "total": total,

      }

      return render(
         request,
         self.template_name,
         context,
      )


   def post(self, request):

      # 1. Validate payment method
      payment_method = request.POST.get("payment_method")

      allowed_payment_methods = {
         Order.PaymentMethod.COD,
         Order.PaymentMethod.SSLCOMMERZ,
      }

      if payment_method not in allowed_payment_methods:
         messages.error(
            request,
            "Please select a valid payment method."
         )

         return redirect("orders:checkout")


      # 2. Validate shipping information
      shipping_method_id = request.session.get(
         "shipping_method_id"
      )
      shipping_address_id = request.session.get(
         "shipping_address_id"
      )

      if not shipping_method_id or not shipping_address_id:
         messages.error(
            request,
            "Choose your delivery details before placing an order.",
         )
         return redirect(
            "shipping:options"
         )


      # 3. Get checkout source
      source = self.get_checkout_source(request)

      coupon_code = request.session.get("coupon_code")


      # 4. Create order
      try:
         if source == "cart":
            order = create_order_from_cart(
               user=request.user,
               shipping_address_id=shipping_address_id,
               shipping_method_id=shipping_method_id,
               payment_method=payment_method,
               coupon_code=coupon_code,
         )

         elif source == "buy_now":
            product_id = request.session.get(
               "buy_now_product_id"
            )
            quantity = request.session.get(
               "buy_now_quantity"
            )

            try:
               product_id = int(product_id)
               quantity = int(quantity)

            except (TypeError, ValueError):
               raise ValidationError(
                  "Your Buy Now session is invalid."
               )

            order = create_order_from_items(
               user=request.user,
               items=[
                  {
                     "product_id": product_id,
                     "quantity": quantity,
                  }
               ],
               shipping_address_id=shipping_address_id,
               shipping_method_id=shipping_method_id,
               payment_method=payment_method,
               coupon_code=coupon_code,
            )

         else:
            raise ValidationError("Invalid checkout source.")


      except ValidationError as exc:
         for error in exc.messages:
            messages.error(request, error)

         return redirect("orders:checkout")


      # 5. Clear checkout session only after successful order creation.
      request.session.pop("shipping_method_id", None)
      request.session.pop("shipping_address_id", None)
      request.session.pop("checkout_source", None)
      request.session.pop("buy_now_product_id", None)
      request.session.pop("buy_now_quantity", None)
      request.session.pop("coupon_code", None)


      # 6. Handle Cash on Delivery
      if payment_method == Order.PaymentMethod.COD:
         messages.success(
            request,
            "Your order has been placed successfully."
         )

         return redirect(
            "orders:detail",
            order_number=order.order_number,
         )

      # 7. Start SSLCommerz payment 
      if payment_method == Order.PaymentMethod.SSLCOMMERZ:
         try:
            result = start_sslcommerz_payment(
               order_id=order.pk,
               user=request.user,
            )

         except ValidationError as exc:
            for error in exc.messages:
               messages.error(request, error)

            return redirect(
               "orders:detail",
               order_number=order.order_number,
            )


         # 8. Redirect customer to SSLCommerz
         gateway_url = result.get("gateway_url")

         if not gateway_url:
            messages.error(
               request,
               "Unable to initialize SSLCommerz payment."
            )

            return redirect(
               "orders:detail",
               order_number=order.order_number,
            )

         return redirect(gateway_url)

            


# Buy Now View
class BuyNowView(LoginRequiredMixin, View):
   def post(self, request, product_id):
      # 1. Read quantity from POST.
      try:
         quantity = int(request.POST.get("quantity", 1))
      except (TypeError, ValueError):
         messages.error(request, "Please enter a valid quantity.")
         return redirect(
            "products:detail", 
            slug="",
         )

      # 2. Validate quantity.
      if quantity < 1:
         messages.error(request, "Quantity must be at least 1.")
         return redirect(
            "products:detail",
            slug="",
         )

      # 3. Fetch the active product.
      product = Product.objects.filter(
         pk=product_id,
         is_active=True,
      ).first()

      if product is None:
         messages.error(request, "This product is unavailable.")
         return redirect("products:list")

      # 4. Validate stock.
      if product.stock < quantity:
         messages.error(
            request,
            f"Insufficient stock. Available: {product.stock}.",
         )
         return redirect(
            "products:detail",
            slug=product.slug,
         )

      # 5. Store the Buy Now intent in the session.
      request.session["checkout_source"] = "buy_now"
      request.session["buy_now_product_id"] = product.pk 
      request.session["buy_now_quantity"] = quantity

      # 6. Remove old shipping selection.
      request.session.pop("shipping_address_id", None)
      request.session.pop("shipping_method_id", None)
      request.session.pop("coupon_code", None)

      messages.success(
         request,
         "Product selected. Please choose your delivery details.",
      )

      return redirect("shipping:options")




# OrderDetailView
class OrderDetailView(LoginRequiredMixin, DetailView):
   model = Order
   template_name = "orders/order_detail.html"
   context_object_name = "order"
   slug_field = "order_number"
   slug_url_kwarg = "order_number"

   def get_queryset(self):
      return (
         super().get_queryset()
         .filter(user=self.request.user)
         .prefetch_related("items")
      )

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)

      context["order_items"] = self.object.items.all()

      return context
   


# Order History View
class OrderHistoryView(LoginRequiredMixin, ListView):
   model = Order
   template_name = "orders/order_history.html"
   context_object_name = "orders"
   paginate_by = 10

   def get_queryset(self):
      return (
         Order.objects
         .filter(user=self.request.user)
         .prefetch_related("items")
         .order_by("-created_at")
      )



# Cancel Order View
class OrderCancelView(LoginRequiredMixin, View):

   def post(self, request, *args, **kwargs):

      order_number = kwargs.get("order_number")

      try:
         order = Order.objects.get(
            order_number=order_number,
            user=request.user,
         )

         cancel_order(
            order_id=order.pk,
            user=request.user,
         )

         messages.success(
            request,
            "Your order has been cancelled successfully."
         )

      except Order.DoesNotExist:
         messages.error(
            request,
            "Order not found."
         )

      except ValidationError as error:
         messages.error(
            request,
            error.messages[0]
         )

      return redirect(
         "orders:detail",
         order_number=order_number,
      )


# Admin Dashboard
class AdminOnlyMixin(LoginRequiredMixin, UserPassesTestMixin):

   def test_func(self):
      return self.request.user.is_superuser


class AdminOrderDashboardView(AdminOnlyMixin, TemplateView):
   template_name = "orders/admin/dashboard.html"

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)

      order_status = Order.objects.aggregate(
         total_orders=Count("id"),

         pending_orders=Count(
            "id",
             filter=Q(status=Order.Status.PENDING),
         ),

         confirmed_orders=Count(
            "id",
            filter=Q(status=Order.Status.CONFIRMED),
         ),

         processing_orders=Count(
            "id",
            filter=Q(status=Order.Status.PROCESSING),
         ),

         shipped_orders=Count(
            "id",
            filter=Q(status=Order.Status.SHIPPED),
         ),

         delivered_orders=Count(
            "id",
            filter=Q(status=Order.Status.DELIVERED),
         ),

         cancelled_orders=Count(
            "id",
            filter=Q(status=Order.Status.CANCELLED),
         ),
      )

      context.update(order_status)

      context["recent_orders"] = (
         Order.objects
         .select_related("user")
         .order_by("-created_at")[:10]
      )

      return context

   


# Admin Order List View
class AdminOrderListView(
   AdminOnlyMixin,
   ListView,
):
   model = Order
   template_name = "orders/admin/order_list.html"
   context_object_name = "orders"
   paginate_by = 20


   def get_queryset(self):

      queryset = (
         Order.objects
         .select_related("user")
         .order_by("-created_at")
      )

      # 1. Order Search
      search_query = self.request.GET.get(
         "q", ""
      ).strip()

      if search_query:

         queryset = queryset.filter(
            Q(order_number__icontains=search_query)
            | Q(user__username__icontains=search_query)
            | Q(user__email__icontains=search_query)
            | Q(shipping_full_name__icontains=search_query)
            | Q(shipping_phone__icontains=search_query)
         )

      # 2. Order Status Filter
      status = self.request.GET.get(
         "status", ""
      ).strip()

      valid_statuses = {
         value for value, label in Order.Status.choices
      }

      if status in valid_statuses:
         queryset = queryset.filter(
            status=status
         )

      return queryset

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)

      context["search_query"] = self.request.GET.get(
         "q", ""
      ).strip()

      context["selected_status"] = self.request.GET.get(
         "status", ""
      ).strip()

      context["status_choices"] = Order.Status.choices

      return context



# Admin Order Detail View
class AdminOrderDetailView(
   AdminOnlyMixin,
   DetailView,
):
   model = Order
   template_name = "orders/admin/order_detail.html"
   context_object_name = "order"
   slug_field = "order_number"
   slug_url_kwarg = "order_number"


   def get_queryset(self):
      return (
         Order.objects
         .select_related("user")
         .prefetch_related("items")
      )

   def get_context_data(self, **kwargs):

      context = super().get_context_data(**kwargs)

      context["order_items"] = (
         self.object.items.all()
      )

      status_form = AdminOrderStatusUpdateForm()

      allowed_statuses = ALLOWED_STATUS_TRANSITIONS.get(
         self.object.status,
         set(),
      )

      status_choices = dict(Order.Status.choices)

      status_form.fields["status"].choices = [
         (status, status_choices[status])
         for status in Order.Status
         if status in allowed_statuses
      ]

      context["status_form"] = status_form

      return context



# Admin Order Status Update View 
class AdminOrderStatusUpdateView(
   AdminOnlyMixin,
   View,
):
   
   def post(self, request, order_number):
      order = get_object_or_404(
         Order,
         order_number=order_number,
      )

      form = AdminOrderStatusUpdateForm(
         request.POST
      )

      if not form.is_valid():
         messages.error(
            request,
            "Please select a valid order status.",
         )

         return redirect(
            "orders:admin_order_detail",
            order_number=order.order_number,
         )

      new_status = form.cleaned_data["status"]

      try:
         updated_order = update_order_status(
            order_id=order.pk,
            new_status=new_status,
         )

      except ValidationError as exc:
         messages.error(
            request,
            " ".join(exc.messages),
         )

         return redirect(
            "orders:admin_order_detail",
            order_number=order.order_number,
         )

      messages.success(
         request,
         (
            f"Order #{updated_order.order_number} "
            f"status updated to "
            f"{updated_order.get_status_display()}."
         ),
      )

      return redirect(
         "orders:admin_order_detail",
         order_number=updated_order.order_number,
      )






   