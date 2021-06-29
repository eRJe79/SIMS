from django.urls import path
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import (
    PieceListView,
    PieceDetailView,
    CreatePieceView,
    UpdateCreatePieceView,
    PieceInstanceUpdate,
    PieceCreate,
    SearchView,
    PieceDelete,
    PieceUpdate,
    PieceInstanceDelete,
    show_instance_form,
    delete_instance,
    create_piece,
    create_piece_instance,
    search_database,
)

urlpatterns = [
    path('piece_list/', PieceListView.as_view(), name='piece'),
    path('piece_detail/<int:pk>', PieceDetailView.as_view(), name='piece-detail'),

    path('inventory/piece-instance-detail/', show_instance_form, name='piece-instance-detail'),
    path('delete-instance/', delete_instance, name="delete-instance"),
    path('search/', search_database, name='search-database'),

    path('create_instance_piece/', create_piece_instance, name='piece-instance-create'),
    path('inventory/update_piece/<int:pk>', UpdateCreatePieceView.as_view(), name='only-piece-update'),
    path('inventory/create/', create_piece, name='piece-create'),

    path('inventory/<int:pk>/update/', PieceUpdate.as_view(), name='piece-update'),
    path('inventory/<int:pk>/delete/', PieceDelete.as_view(), name='piece-delete'),
    path('inventory/delete/', PieceInstanceDelete.as_view(), name='piece-instance-delete'),
]