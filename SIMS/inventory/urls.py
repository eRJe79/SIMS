from django.urls import path

from .views import (
    PieceListView,
    PieceDetailView,
    PieceCreate,
    PieceDelete,
    PieceUpdate,
    create_piece,
)

urlpatterns = [
    path('piece_list/', PieceListView.as_view(), name='piece'),
    path('piece_detail/<int:pk>', PieceDetailView.as_view(), name='piece-detail'),
    path('create-piece/', create_piece, name='create-piece'),

    path('inventory/create/', PieceCreate.as_view(), name='piece-create'),
    path('inventory/<int:pk>/update/', PieceUpdate.as_view(), name='piece-update'),
    path('inventory/<int:pk>/delete/', PieceDelete.as_view(), name='piece-delete'),
]