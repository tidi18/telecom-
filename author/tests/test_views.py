from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from author.models import Author
from datetime import date


class AuthorViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            email="test@gmail.com",
            password="12qwaszx12qwaszx"
        )




        self.author = Author.objects.create(
            first_name="test first name",
            last_name="test last name",
            biography="test biography",
            date_of_birth=date(1828, 9, 9),
            date_of_death=date(1928, 9, 9),
        )

    def test_get_authors_list(self):

        url = reverse("author-list")
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


    def test_auth_required(self):
        url = reverse("author-list")

        self.client.force_authenticate(user=None)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)


    def test_create_author(self):
        self.url = reverse("author-create")

        self.client.force_authenticate(user=self.user)

        data = {
            "first_name": "Leo",
            "last_name": "Tolstoy",
            "biography": "Russian writer",
            "date_of_birth": "1828-09-09"
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 201)


    def test_create_author_unauthenticated(self):
        self.url = reverse("author-create")

        self.client.force_authenticate(user=None)  # убираем авторизацию

        data = {
            "first_name": "Leo",
            "last_name": "Tolstoy",
            "biography": "Russian writer",
            "date_of_birth": "1828-09-09"
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 401)

    def test_delete_author_authenticated(self):
        self.url = reverse("author-delete", args=[self.author.id])

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Author.objects.count(), 0)

    def test_delete_author_unauthenticated(self):
        self.url = reverse("author-delete", args=[self.author.id])

        self.client.force_authenticate(user=None)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 401)

    def test_update_author_authenticated(self):
        self.url = reverse("author-update", args=[self.author.id])

        self.client.force_authenticate(user=self.user)

        data = {
            "last_name": "Tolstoy Updated"
        }

        response = self.client.patch(self.url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.author.refresh_from_db()
        self.assertEqual(self.author.last_name, "Tolstoy Updated")

    def test_update_author_unauthenticated(self):
        self.url = reverse("author-update", args=[self.author.id])

        self.client.force_authenticate(user=None)

        data = {
            "last_name": "Tolstoy Updated2"
        }

        response = self.client.patch(self.url, data, format="json")

        self.assertEqual(response.status_code, 401)

    def test_get_author_detail_authenticated(self):
        author_from_db = Author.objects.get(id=self.author.id)

        self.url = reverse("author-detail", args=[self.author.id])

        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "test first name")
        self.assertEqual(response.data["last_name"], "test last name")
        self.assertEqual(response.data["biography"], "test biography")
        self.assertEqual(author_from_db.date_of_birth, date(1828, 9, 9))
        self.assertEqual(author_from_db.date_of_death, date(1928, 9, 9))

    def test_get_author_detail_unauthenticated(self):
        self.url = reverse("author-detail", args=[self.author.id])

        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)



