from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

   phone = models.CharField(max_length=20, blank=True)
   profile_picture = models.ImageField(
      upload_to="profiles/",
      blank=True,
      null=True,
   )
   date_of_birth = models.DateField(
      blank=True,
      null=True,
   )
   address = models.TextField(blank=True)

   def __str__(self):
      return self.username