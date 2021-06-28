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
    PieceDelete,
    PieceUpdate,
    PieceInstanceDelete,
    show_instance_form,
    delete_instance,
    update_instance,
    create_piece,
)

urlpatterns = [
    path('piece_list/', PieceListView.as_view(), name='piece'),
    path('piece_detail/<int:pk>', PieceDetailView.as_view(), name='piece-detail'),

    path('inventory/piece-instance-detail/', show_instance_form, name='piece-instance-detail'),
    path('delete-instance/', delete_instance, name="delete-instance"),
    path('update-instance/', update_instance, name="update-instance"),

    path('create_instance_piece/', CreatePieceView.as_view(), name='piece-instance-create'),
    path('inventory/update_piece/<int:pk>', UpdateCreatePieceView.as_view(), name='only-piece-update'),
    path('inventory/create/', create_piece, name='piece-create'),
    path('inventory/<int:pk>/update/', PieceUpdate.as_view(), name='piece-update'),
    path('inventory/<int:pk>/delete/', PieceDelete.as_view(), name='piece-delete'),
    path('inventory/delete/', PieceInstanceDelete.as_view(), name='piece-instance-delete'),
]