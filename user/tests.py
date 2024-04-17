from django.test import TestCase
from .models import NilvaUser


class NilvaUserModelTestCase(TestCase):
    def test_user_creation(self):
        username = "testuser"
        email = "test@example.com"
        user = NilvaUser.objects.create(username=username, email=email)
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertEqual(user.permissions, NilvaUser.NORMAL)

    def test_user_str_method(self):
        username = "testuser"
        user = NilvaUser.objects.create(username=username, email="test@example.com")
        self.assertEqual(str(user), username)
