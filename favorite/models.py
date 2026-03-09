from django.contrib.auth.models import User
from django.db import models
from book.models import Book


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.book}"

    class Meta:
        unique_together = ("user", "book")

