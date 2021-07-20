from django.urls import path
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import (
    PieceListView,
    PieceCreate,
    show_piece,
    search_piece_database,
    KitCreate,
    KitList,
    show_kit,
    database_csv,
)

urlpatterns = [
    path('search/', search_piece_database, name='search-piece-database'),

    path('piece_list/', PieceListView.as_view(), name='piece'),
    path('piece_detail/<primary_key>', show_piece, name='piece-detail'),
    path('inventory/create/', PieceCreate.as_view(), name='piece-create'),

    path('kit_form/', KitCreate.as_view(), name='kit-create'),
    path('kit_list/', KitList.as_view(), name='kit'),
    path('kit_detail/<primary_key>', show_kit, name='kit-detail'),

    path('database_csv', database_csv, name='database_csv'),
]