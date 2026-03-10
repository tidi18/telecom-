from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from book.models import Book
from favorite.models import Favorite
from datetime import date


class FavoriteAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass123")

        self.book1 = Book.objects.create(title="Book 1", summary="Summary", isbn="1234567890123", publication_date=date(2020,1,1))
        self.book2 = Book.objects.create(title="Book 2", summary="Summary", isbn="1234567890124", publication_date=date(2021,1,1))

        self.list_url = reverse("favorite-list")
        self.create_url = reverse("favorite-create")
        self.clear_url = reverse("favorites-clear")

    def test_list_favorites_authenticated(self):
        Favorite.objects.create(user=self.user, book=self.book1)
        Favorite.objects.create(user=self.user2, book=self.book2)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['book'], self.book1.id)

    def test_list_favorites_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 401)

    def test_create_favorite(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.create_url, {"book": self.book1.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Favorite.objects.filter(user=self.user).count(), 1)

    def test_create_duplicate_favorite(self):
        Favorite.objects.create(user=self.user, book=self.book1)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.create_url, {"book": self.book1.id})
        self.assertEqual(response.status_code, 400)
        self.assertIn("already in your favorites", str(response.data))

    def test_create_favorite_unauthenticated(self):
        response = self.client.post(self.create_url, {"book": self.book1.id})
        self.assertEqual(response.status_code, 401)

    def test_delete_favorite(self):
        fav = Favorite.objects.create(user=self.user, book=self.book1)
        self.client.force_authenticate(user=self.user)
        url = reverse("favorite-delete", args=[fav.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Favorite.objects.filter(user=self.user).count(), 0)

    def test_delete_favorite_unauthenticated(self):
        fav = Favorite.objects.create(user=self.user, book=self.book1)
        url = reverse("favorite-delete", args=[fav.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_clear_favorites(self):
        Favorite.objects.create(user=self.user, book=self.book1)
        Favorite.objects.create(user=self.user, book=self.book2)

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.clear_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Favorite.objects.filter(user=self.user).count(), 0)

    def test_clear_favorites_unauthenticated(self):
        response = self.client.delete(self.clear_url)
        self.assertEqual(response.status_code, 401)