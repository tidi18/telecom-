from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from book.models import Book, Genre
from author.models import Author
from datetime import date

class BookFilterAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)


        self.author1 = Author.objects.create(first_name="Leo", last_name="Tolstoy", biography="Russian writer", date_of_birth=date(1828,9,9))
        self.author2 = Author.objects.create(first_name="Fyodor", last_name="Dostoevsky", biography="Russian writer", date_of_birth=date(1821,11,11))

        self.genre1 = Genre.objects.create(name="Fiction")
        self.genre2 = Genre.objects.create(name="Classic")

        self.book1 = Book.objects.create(title="War and Peace", summary="Epic novel", isbn="1234567890123", publication_date=date(1869,1,1))
        self.book1.authors.set([self.author1])
        self.book1.genres.set([self.genre1])

        self.book2 = Book.objects.create(title="Crime and Punishment", summary="Another epic", isbn="1234567890124", publication_date=date(1866,1,1))
        self.book2.authors.set([self.author2])
        self.book2.genres.set([self.genre2])

        self.url = reverse("books-filter")

    def test_filter_by_author_id(self):
        response = self.client.get(self.url, {"authors": self.author1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "War and Peace")

    def test_filter_by_genre_id(self):
        response = self.client.get(self.url, {"genres": self.genre2.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Crime and Punishment")

    def test_filter_by_publication_date_range(self):
        response = self.client.get(self.url, {"publication_date_after": "1867-01-01", "publication_date_before": "1870-01-01"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "War and Peace")

    def test_search_by_title(self):
        response = self.client.get(self.url, {"title": "Crime"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Crime and Punishment")

    def test_search_by_author_last_name(self):
        response = self.client.get(self.url, {"author_last_name": "Tolstoy"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "War and Peace")