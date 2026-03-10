from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

class AuthAPITest(APITestCase):

    def setUp(self):
        self.register_url = reverse("register")
        self.logout_url = reverse("logout")
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "12qwaszx12qwaszx",
            "password2": "12qwaszx12qwaszx"
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, "testuser")

    def test_logout_user(self):
        response = self.client.post(self.register_url, self.user_data)
        refresh_token = response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        response = self.client.post(self.logout_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response.data["detail"], "Successfully logged out.")

    def test_logout_without_refresh_token(self):
        response = self.client.post(self.register_url, self.user_data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        response = self.client.post(self.logout_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Refresh token required.")

    def test_logout_unauthenticated(self):
        response = self.client.post(self.logout_url, {"refresh": "dummy"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)