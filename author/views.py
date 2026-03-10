from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Author
from .serializers import AuthorSerializer, AuthorCreateSerializer, AuthorUpdateSerializer, AuthorDetailSerializer


class AuthorCreateAPIView(CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorCreateSerializer
    permission_classes = [IsAuthenticated]


class AuthorListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetailAPIView(RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer
    permission_classes = [IsAuthenticated]


class AuthorUpdateAPIView(UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorUpdateSerializer
    permission_classes = [IsAuthenticated]


class AuthorDeleteAPIView(DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer
    permission_classes = [IsAuthenticated]