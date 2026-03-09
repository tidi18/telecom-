from django.urls import path
from .views import FavoriteListView, FavoriteCreateView, FavoriteDeleteView, FavoriteClearView

urlpatterns = [
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/create/', FavoriteCreateView.as_view(), name='favorite-create'),
    path('favorites/<int:pk>/delete/', FavoriteDeleteView.as_view(), name='favorite-delete'),
    path('favorites/clear/', FavoriteClearView.as_view(), name='favorites-clear'),

]