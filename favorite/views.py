from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import serializers
from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteListView(ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Favorite.objects.none()
        return Favorite.objects.filter(user=self.request.user)


class FavoriteCreateView(CreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        book = serializer.validated_data['book']


        if Favorite.objects.filter(user=user, book=book).exists():
            raise serializers.ValidationError("This book is already in your favorites")

        serializer.save(user=user)


class FavoriteDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Favorite.objects.none()
        return Favorite.objects.filter(user=self.request.user)

class FavoriteClearView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        Favorite.objects.filter(user=request.user).delete()
        return Response({"message": "Favorites cleared"})