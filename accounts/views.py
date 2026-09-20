from django.shortcuts import render, redirect
from django.contrib import messages 
from .forms import RegisterForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm ,PasswordChangeForm 
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required


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



def user_logout(request):
   logout(request)

   messages.success(
      request,
      "You have been logged out."
   )

   return redirect("accounts:login")




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




"""
8. আপনার code-এর architecture

বর্তমানে আপনার Accounts app-এর structure আসলে সুন্দর একটা backend concept দেখাচ্ছে:
                    accounts
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
    Register         Login          Logout
        │              │              │
   RegisterForm   AuthenticationForm  logout()
        │              │
        ↓              ↓
      User          Session
        │
        ├───────────────┐
        ↓               ↓
     Profile       Edit Profile
                         │
                  ProfileUpdateForm
                         │
                         ↓
                   request.user
                         │
                         ↓
                    form.save()
                         │
                         ↓
                   User updated

        User
          │
          ↓
   Change Password
          │
 PasswordChangeForm
          │
          ↓
     form.save()
          │
          ↓
update_session_auth_hash()

1. এটা শুধু "Django code" না—
এখানে আপনি ইতিমধ্যে Authentication, Session, Form Validation,
ModelForm, File Upload, Authorization—এই backend concepts শিখছেন।


2. আপনার এখন এই conceptsগুলো জানা হয়ে যাচ্ছে:
Function-Based View = register(), user_login()
Authentication =	AuthenticationForm
Login	= login()
Logout =	logout()
Authorization =	@login_required
ModelForm =	RegisterForm, ProfileUpdateForm
Existing object update = instance=request.user
File upload	= request.FILES
Password management	= PasswordChangeForm
Session	= login() / logout()
Session preservation	= update_session_auth_hash()
Flash messages	= messages.success()
POST/GET handling	= request.method
Validation	= form.is_valid()

"""