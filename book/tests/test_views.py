from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from author.models import Author
from book.models import Book, Genre
from datetime import date

class BookViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            email="test@gmail.com",
            password="12qwaszx12qwaszx"
        )

        self.author = Author.objects.create(
        first_name="Leo",
        last_name="Tolstoy",
        biography="Russian writer",
        date_of_birth=date(1828, 9, 9)
        )

        self.author2 = Author.objects.create(
            first_name="Fyodor",
            last_name="Dostoevsky",
            biography="Russian writer",
            date_of_birth=date(1821, 11, 11)
        )

        self.genre1 = Genre.objects.create(name="fantasy")
        self.genre2 = Genre.objects.create(name="classic")


    def test_create_book(self):
        self.url = reverse("book-create")

        self.client.force_authenticate(user=self.user)

        data = {
            "authors": [self.author.id, self.author2.id],
            "title": "test book",
            "summary": "test summary",
            "isbn": "1234567899876",
            "publication_date": "2020-09-09",
            "genres": [self.genre1.id, self.genre2.id],

        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 201)


    def test_create_book_unauthenticated(self):
        self.url = reverse("book-create")

        self.client.force_authenticate(user=None)

        data = {
            "authors": [self.author.id, self.author2.id],
            "title": "test book",
            "summary": "test summary",
            "isbn": "1234567899876",
            "publication_date": "2020-09-09",
            "genres": [self.genre1.id, self.genre2.id],

        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_get_book_list(self):

        url = reverse("book-list")
        self.client.force_authenticate(user=self.user)

        book = Book.objects.create(
            title="War and Peace",
            summary="Epic novel",
            isbn="1234567890123",
            publication_date=date(1869, 1, 1)
        )

        book.authors.set([self.author, self.author2])
        book.genres.set([self.genre1, self.genre2])
        book_from_db = Book.objects.get(id=book.id)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(book_from_db.title, "War and Peace")
        self.assertEqual(book_from_db.summary, "Epic novel")
        self.assertEqual(book_from_db.isbn, "1234567890123")
        self.assertEqual(book_from_db.publication_date, date(1869, 1, 1))


    def test_book_required(self):
        url = reverse("book-list")

        self.client.force_authenticate(user=None)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)


    def test_delete_book_authenticated(self):
        book = Book.objects.create(
            title="War and Peace",
            summary="Epic novel",
            isbn="1234567890123",
            publication_date=date(1869, 1, 1)
        )

        book.authors.set([self.author, self.author2])
        book.genres.set([self.genre1, self.genre2])
        book.refresh_from_db()


        self.url = reverse("book-delete", args=[book.id])

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_unauthenticated(self):

        book = Book.objects.create(
            title="War and Peace",
            summary="Epic novel",
            isbn="1234567890123",
            publication_date=date(1869, 1, 1)
        )

        book.authors.set([self.author, self.author2])
        book.genres.set([self.genre1, self.genre2])
        book.refresh_from_db()

        self.url = reverse("book-delete", args=[book.id])

        self.client.force_authenticate(user=None)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 401)


    def test_update_book_authenticated(self):
        book = Book.objects.create(
            title="War and Peace",
            summary="Epic novel",
            isbn="1234567890123",
            publication_date=date(1869, 1, 1)
        )

        book.authors.set([self.author, self.author2])
        book.genres.set([self.genre1, self.genre2])


        self.url = reverse("book-update", args=[book.id])

        self.client.force_authenticate(user=self.user)

        data = {
            "title": " test book updated"
        }

        response = self.client.patch(self.url, data, format="json")

        self.assertEqual(response.status_code, 200)
        book.refresh_from_db()
        self.assertEqual(book.title, "test book updated")

    def test_update_book_unauthenticated(self):
        book = Book.objects.create(
            title="War and Peace",
            summary="Epic novel",
            isbn="1234567890123",
            publication_date=date(1869, 1, 1)
        )

        book.authors.set([self.author, self.author2])
        book.genres.set([self.genre1, self.genre2])

        self.url = reverse("book-update", args=[book.id])

        self.client.force_authenticate(user=None)

        data = {
            "last_name": "Tolstoy Updated"
        }

        response = self.client.patch(self.url, data, format="json")

        self.assertEqual(response.status_code, 401)


    def test_get_book_detail_authenticated(self):
        book = Book.objects.create(
            title="War and Peace",
            summary="Epic novel",
            isbn="1234567890123",
            publication_date=date(1869, 1, 1)
        )

        book.authors.set([self.author, self.author2])
        book.genres.set([self.genre1, self.genre2])
        book.refresh_from_db()

        book_from_db = Book.objects.get(id=book.id)


        self.url = reverse("book-detail", args=[book.id])

        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "War and Peace")
        self.assertEqual(response.data["summary"], "Epic novel")
        self.assertEqual(response.data["isbn"], "1234567890123")
        self.assertEqual(book_from_db.publication_date, date(1869, 1, 1))


    def test_get_book_detail_unauthenticated(self):
        book = Book.objects.create(
            title="War and Peace",
            summary="Epic novel",
            isbn="1234567890123",
            publication_date=date(1869, 1, 1)
        )

        book.authors.set([self.author, self.author2])
        book.genres.set([self.genre1, self.genre2])
        book.refresh_from_db()

        self.url = reverse("book-detail", args=[book.id])

        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)







