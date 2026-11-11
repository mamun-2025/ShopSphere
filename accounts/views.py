
from django.shortcuts import render, redirect
from django.contrib import messages 
from .forms import RegisterForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm ,PasswordChangeForm 
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.db.models import Q 



# 1. Customer Register 
def register(request):
   if request.method == "POST":
      form = RegisterForm(request.POST)
      
      if form.is_valid():
         form.save()

         messages.success(
            request,
            "Your registration was successful. You can now log in.",
         )
         return redirect("accounts:login")

   else:
      form = RegisterForm()

   return render(
      request,
      "accounts/register.html",
      {
         "form": form,
      },
   )



# 2. Customer Login 
def user_login(request):
   if request.method == "POST":
      form = AuthenticationForm(request, data=request.POST)

      if form.is_valid():

         user = form.get_user()

         login(request, user)

         messages.success(
            request,
            "Login successful."
         )
         return redirect("accounts:profile")

   else:
      form = AuthenticationForm()

   for field in form.fields.values():
      field.widget.attrs["class"] = "form-control"

   return render(
      request,
      "accounts/login.html",
      {
         "form": form,
      },
   )



# 3. Customer Logout
def user_logout(request):
   logout(request)

   messages.success(
      request,
      "You have been logged out."
   )

   return redirect("accounts:login")




# 4. Customer Profile 
@login_required
def profile(request):
   return render(
      request,
      "accounts/profile.html",
   )



# 5. Customer Edit Profile
@login_required
def edit_profile(request):

   if request.method == "POST":
      form = ProfileUpdateForm(
         request.POST,
         request.FILES,
         instance=request.user,
      )

      if form.is_valid():
         form.save()

         messages.success(
            request,
            "Your profile has been updated successfully.",
         )
         return redirect("accounts:profile")

   else:
      form = ProfileUpdateForm(
         instance=request.user,
      )

   return render(
      request,
      "accounts/edit_profile.html",
      {
         "form": form,
      },
   )



# 6. Customer Change Password
@login_required
def change_password(request):

   if request.method == "POST":

      form = PasswordChangeForm(
         user=request.user,
         data=request.POST,
      )

      if form.is_valid():
         user = form.save()

         update_session_auth_hash(
            request,
            user,
         )

         messages.success(
            request,
            "Your password has been changed successfully.",
         )

         return redirect("accounts:profile")

   else:
      form = PasswordChangeForm(
         user=request.user,
      )

   for field in form.fields.values():
      field.widget.attrs["class"] = "form-control"
      

   return render(
      request,
      "accounts/change_password.html",
      {
         "form": form
      },
   )




User = get_user_model()


# Admin Customer List View
class AdminCustomerListView(UserPassesTestMixin, ListView):
   model = User
   template_name = "accounts/admin/customer_list.html"
   context_object_name = "customers"
   paginate_by = 10

   def test_func(self):
      return self.request.user.is_superuser

   def get_queryset(self):
      queryset = User.objects.filter(
         is_staff=False,
         is_superuser=False,
      ).order_by("-date_joined")

      search_query = self.request.GET.get(
         "q", ""
      ).strip()

      if search_query:
         queryset = queryset.filter(
            Q(username__icontains=search_query)
            | Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(phone__icontains=search_query)
         )

      return queryset


   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)

      context["search_query"] = self.request.GET.get(
         "q", ""
      )

      context["total_customers"] = User.objects.filter(
         is_staff=False,
         is_superuser=False,
      ).count()

      return context




# Admin Customer Detail View
class AdminCustomerDetailView(UserPassesTestMixin, DetailView):

   model = User 
   template_name = "accounts/admin/customer_detail.html"
   context_object_name = "customer"

   def test_func(self):
      return self.request.user.is_superuser

   def get_queryset(self):
      return User.objects.filter(
         is_staff=False,
         is_superuser=False,
      )



   