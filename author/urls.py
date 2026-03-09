from django.urls import path
from .views import AuthorListAPIView, AuthorCreateAPIView, AuthorDetailAPIView, AuthorUpdateAPIView, AuthorDeleteAPIView

urlpatterns = [
    path('authors/', AuthorListAPIView.as_view(), name='author-list'),
    path('authors/create/', AuthorCreateAPIView.as_view(), name='author-create'),
    path('authors/<int:pk>/', AuthorDetailAPIView.as_view(), name='author-detail'),
    path('authors/<int:pk>/update/', AuthorUpdateAPIView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', AuthorDeleteAPIView.as_view(), name='author-delete'),
]