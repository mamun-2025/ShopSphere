

from django import forms 
from django.contrib.auth.forms import UserCreationForm 
from .models import User 

class RegisterForm(UserCreationForm):

   class Meta:
      model = User 
      fields = (
         "username",
         "email",
         "phone",
         "password1",
         "password2",
      )

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      for fieldname in self.fields.values():
         fieldname.widget.attrs["class"] = "form-control"


class ProfileUpdateForm(forms.ModelForm):
   class Meta:
      model = User
      fields = (
         "first_name",
         "last_name",
         "email",
         "phone",
         "date_of_birth",
         "address",
         "profile_picture",
      )  

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      for field in self.fields.values():
         field.widget.attrs["class"] = "form-control"