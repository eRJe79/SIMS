from django.urls import path

from .views import (
    PieceListView,
    PieceDetailView,
    CategoryListView,
    CategoryDetailView,
)

urlpatterns = [
    path('inventory/', PieceListView.as_view(), name='piece'),
    path('inventory/<int:pk>', PieceDetailView.as_view(), name='piece-detail'),
    path('inventory/', CategoryListView.as_view(), name='category'),
    path('inventory/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
]