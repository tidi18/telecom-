from datetime import date
from django.contrib.auth.models import User
from book.models import Book, Genre
from author.models import Author
from book.tasks import notify_new_books, notify_anniversary_books
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta


class TaskTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@gmail.com", password="12qwaszx12qwaszx")

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


    def test_new_books_notification(self):
        book = Book.objects.create(
            created_at=timezone.now(),
            title="War and Peace",
            summary="Epic novel",
            isbn="1234567890123",
            publication_date=date(1869, 1, 1)
        )

        book.authors.set([self.author, self.author2])
        book.genres.set([self.genre1, self.genre2])

        result = notify_new_books()

        self.assertIn("Уведомления о новых книгах отправлены", result)


    def test_no_new_books(self):
        book = Book.objects.create(
            created_at=timezone.now(),
            title="War and Peace",
            summary="Epic novel",
            isbn="1234567890123",
            publication_date=date(1869, 1, 1)
        )

        book.created_at = timezone.now() - timedelta(days=2)
        book.save()

        book.authors.set([self.author, self.author2])
        book.genres.set([self.genre1, self.genre2])

        result = notify_new_books()

        self.assertEqual(result, "Нет новых книг")

    def test_anniversary_book(self):
        today = date.today()

        book = Book.objects.create(
            created_at=timezone.now(),
            title="War and Peace",
            summary="Epic novel",
            isbn="1234567890123",
            publication_date=date(today.year - 10, today.month, today.day)
        )

        book.authors.set([self.author, self.author2])
        book.genres.set([self.genre1, self.genre2])

        result = notify_anniversary_books()
        self.assertEqual(result, "Юбилейные книги найдены")


    def test_no_anniversary_book(self):
        today = date.today()

        book = Book.objects.create(
            created_at=timezone.now(),
            title="War and Peace",
            summary="Epic novel",
            isbn="1234567890123",
            publication_date=date(today.year - 1, today.month, today.day)
        )

        book.authors.set([self.author, self.author2])
        book.genres.set([self.genre1, self.genre2])

        result = notify_anniversary_books()
        self.assertEqual(result, "Проверка юбилейных книг выполнена")







