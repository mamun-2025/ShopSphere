
from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


# =====================================================
# 1. User Model Tests
# =====================================================
class UserModelTests(TestCase):

   def setUp(self):
      self.user = User.objects.create_user(
         username="testuser",
         email="test@example.com",
         password="TestPassword123!",
         phone="01964766244",
      )

   def test_user_creation(self):
      self.assertEqual(self.user.username, "testuser")
      self.assertEqual(self.user.email, "test@example.com")

   def test_user_password_is_hashed(self):
      self.assertNotEqual(
         self.user.password,
         "TestPassword123!"
      )

      self.assertTrue(
         self.user.check_password("TestPassword123!")
      )

   def test_user_string_representation(self):
      self.assertEqual(str(self.user), "testuser")

   def test_optional_fields_can_be_blank(self):
      user = User.objects.create_user(
         username="anotheruser",
         password="TestPassword123!",
      )

      self.assertEqual(user.phone, "")
      self.assertEqual(user.address, "")