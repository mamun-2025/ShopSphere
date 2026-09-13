from django.shortcuts import render, redirect
from django.contrib import messages 
from .forms import RegisterForm 
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, logout, authenticate 


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


def user_login(request):
   if request.method == "POST":
      form = AuthenticationForm(request, data=request.POST)

      if form.is_valid():
         username = form.cleaned_data.get("username")
         password = form.cleaned_data.get("password")

         user = authenticate(
            username=username,
            password=password,
         )

         if user is not None:
            login(request, user)

            messages.success(
               request,
               "Login successful."
            )

            return redirect("profile")

      else:
         form = AuthenticationForm()

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

   return redirect("accounts:login")