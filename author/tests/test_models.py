from django.test import TestCase
from author.models import Author
from datetime import date


class AuthorModelTest(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            first_name="Leo",
            last_name="Tolstoy",
            biography="Russian writer",
            date_of_birth=date(1828, 9, 9)
        )

    def test_author_creation(self):
        """Проверка создания автора"""
        self.assertEqual(self.author.first_name, "Leo")
        self.assertEqual(self.author.last_name, "Tolstoy")

    def test_author_str(self):
        """Проверка метода __str__"""
        self.assertEqual(str(self.author), "Leo Tolstoy")

    def test_date_of_death_optional(self):
        """Поле date_of_death не обязательное"""
        self.assertIsNone(self.author.date_of_death)