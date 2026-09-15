from django.shortcuts import render, redirect
from django.contrib import messages 
from .forms import RegisterForm 
from django.contrib.auth.forms import AuthenticationForm ,PasswordChangeForm 
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.contrib.auth import update_session_auth_hash


def register(request):
   if request.method == "POST":
      form = RegisterForm(request.POST)
      
      if form.is_valid():
         form.save()

         messages.success(
            request,
            "Your registration was successful. You can now log in.",
         )
         return redirect("login")

   else:
      form = RegisterForm()

   return render(
      request,
      "accounts/register.html",
      {
         "form": form,
      },
   )


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
         return redirect("profile")

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

def user_logout(request):
   logout(request)

   messages.success(
      request,
      "You have been logged out."
   )

   return redirect("login")



@login_required
def profile(request):
   return render(
      request,
      "accounts/profile.html",
   )



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
         return redirect("profile")

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

         return redirect("profile")

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
