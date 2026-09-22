
from django.core.exceptions import ValidationError


def validate_file_size(file):

   max_size = 5 * 1024 * 1024

   if file.size > max_size:
      raise ValidationError(
         "File size must be 5 MB or Less."
      )