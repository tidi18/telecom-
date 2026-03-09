from rest_framework import serializers
from .models import Book, Genre
from author.models import Author
from author.serializers import AuthorSerializer




class BookCreateSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)


    class Meta:
        model = Book
        fields = ['title', 'summary', 'isbn', 'publication_date', 'authors', 'genres']


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = ['id', 'authors', 'title']
        read_only_fields = ['id']


class BookDetailSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)


    class Meta:
        model = Book
        fields = ['id','title', 'summary', 'isbn', 'publication_date', 'authors', 'genres']
        read_only_fields = ['id']


class BookUpdateSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)


    class Meta:
        model = Book
        fields = ['title', 'summary', 'isbn', 'publication_date', 'authors', 'genres']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class BookFilterSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'genres', 'publication_date']