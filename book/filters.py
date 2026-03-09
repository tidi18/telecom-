import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):

    publication_date_after = django_filters.DateFilter(
        field_name="publication_date",
        lookup_expr="gte"
    )

    publication_date_before = django_filters.DateFilter(
        field_name="publication_date",
        lookup_expr="lte"
    )

    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains"
    )

    author_last_name = django_filters.CharFilter(
        field_name="authors__last_name", lookup_expr="icontains"
    )

    class Meta:
        model = Book
        fields = [
            "authors",
            "genres",
            "title",
            "author_last_name",
            'publication_date_before',
            'publication_date_after'

        ]