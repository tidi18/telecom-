from django.db import models
from author.models import Author


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=200)
    summary = models.TextField()
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        authors_names = ", ".join([str(author) for author in self.authors.all()])
        return f"{authors_names} {self.title}"