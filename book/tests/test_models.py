from django.test import TestCase
from book.models import Book, Genre
from author.models import Author
from datetime import date


class BookModelTest(TestCase):

    def setUp(self):
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
        book = Book.objects.create(
            title="War and Peace",
            summary="Epic novel",
            isbn="1234567890123",
            publication_date=date(1869, 1, 1)
        )

        book.authors.set([self.author, self.author2])
        book.genres.set([self.genre1, self.genre2])
        book_from_db = Book.objects.get(id=book.id)

        self.assertEqual(book_from_db.title, "War and Peace")
        self.assertEqual(book_from_db.summary, "Epic novel")
        self.assertEqual(book_from_db.isbn, "1234567890123")
        self.assertEqual(book_from_db.publication_date, date(1869, 1, 1))

        authors = list(book_from_db.authors.all())
        self.assertIn(self.author, authors)
        self.assertIn(self.author2, authors)

        genres = list(book_from_db.genres.all())
        self.assertIn(self.genre1, genres)
        self.assertIn(self.genre2, genres)

        expected_str = f"{self.author} , {self.author2} War and Peace"
        self.assertEqual(str(book_from_db), str(book_from_db))