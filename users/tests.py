from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@test.com"
        )

    def test_register(self):
        url = reverse("users:register")
        data = {
            "username": "newuser",
            "password": "newpass123",
            "email": "new@test.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_login(self):
        url = reverse("users:login")
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_refresh(self):
        login_url = reverse("users:login")
        tokens = self.client.post(login_url, {"username": "testuser", "password": "testpass123"}).data
        url = reverse("users:token_refresh")
        response = self.client.post(url, {"refresh": tokens["refresh"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_profile_unauthenticated(self):
        url = reverse("users:profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_update(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:profile")
        data = {"username": "testuser", "telegram_chat_id": "123456789"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["telegram_chat_id"], "123456789")
