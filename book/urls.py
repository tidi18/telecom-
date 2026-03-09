from django.urls import path
from .views import BookListAPIView, BookCreateAPIView, BookDetailAPIView, BookUpdateAPIView, BookDeleteAPIView

urlpatterns = [
    path('books/', BookListAPIView.as_view(), name='book-list'),
    path('books/create/', BookCreateAPIView.as_view(), name='book-create'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', BookUpdateAPIView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteAPIView.as_view(), name='book-delete'),
]