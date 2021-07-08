from django.urls import path
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import (
    PieceListView,
    show_instance_form,
    delete_instance,
    create_piece,
    show_piece,
    create_piece_instance,
    update_instance,
    all_piece_instance,
    search_piece_database,
    search_instance_database,
    create_kit,
)

urlpatterns = [
    path('search/', search_piece_database, name='search-piece-database'),
    path('search_instance/', search_instance_database, name='search-instance-database'),

    path('piece_list/', PieceListView.as_view(), name='piece'),
    path('piece_detail/<primary_key>', show_piece, name='piece-detail'),
    path('inventory/create/', create_piece, name='piece-create'),

    path('piece_instance_list', all_piece_instance, name="piece-instance-list"),
    path('create_instance_piece/', create_piece_instance, name='piece-instance-create'),
    path('piece_instance_detail/<primary_key>', show_instance_form, name='piece-instance-detail'),
    path('delete_piece_instance/<instance_id>', delete_instance, name="delete-piece-instance"),
    path('update_piece_instance/<instance_id>', update_instance, name='update-piece-instance'),

    path('create_kit/', create_kit, name='kit-create'),
]