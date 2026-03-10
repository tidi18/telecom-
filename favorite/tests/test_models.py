from django.contrib.auth.models import User
from django.test import TestCase
from book.models import Book, Genre
from author.models import Author
from favorite.models import Favorite
from datetime import date

class FavoriteModelTest(TestCase):

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

        self.book = Book.objects.create(
            title="War and Peace",
            summary="Epic novel",
            isbn="1234567890123",
            publication_date=date(1869, 1, 1)
        )

        self.book.authors.set([self.author, self.author2])
        self.book.genres.set([self.genre1, self.genre2])


    def test_create_favorite(self):
        favorite = Favorite.objects.create(
            user=self.user,
            book=self.book,
        )

        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.book, self.book)





