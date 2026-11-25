

from django import forms 
from .models import Review

class ReviewForm(forms.ModelForm):

   class Meta:
      model = Review

      fields = [
         "rating",
         "comment",
      ]

      widgets = {

         "rating": forms.Select(
            choices= [
               (1, "⭐"),
               (2, "⭐⭐"),
               (3, "⭐⭐⭐"),
               (4, "⭐⭐⭐⭐"),
               (5, "⭐⭐⭐⭐⭐"),
            ],
            attrs={
               "class": "form-select",
            },
         ),

         "comment": forms.Textarea(
            attrs={
               "class": "form-control",
               "rows": 4,
               "placeholder": "Write your review",
            },
         ),
      }

   def clean_comment(self):
      comment = self.cleaned_data["comment"].strip()

      if not comment:
         raise forms.ValidationError(
            "Review comment cannot be empty."
         )
      
      return comment
   
