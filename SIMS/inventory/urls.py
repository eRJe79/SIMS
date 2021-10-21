from django.urls import path
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import (
    PieceListView,
    show_instance_form,
    delete_instance,
    PieceCreate,
    show_piece,
    update_piece,
    clone_piece,
    show_piece_history,
    PieceInstanceCreate,
    update_instance,
    clone_instance,
    all_piece_instance,
    show_instance_history,
    search_piece_database,
    search_instance_database,
    GroupAssemblyCreate,
    GroupAssemblyListView,
    show_groupassembly,
    update_computer_assembly,
    KitCreate,
    KitList,
    show_kit,
    update_kit,
    show_assembly_history,
    database_csv,
    load_item_1,
    load_item_2,
    load_second_location,
    load_third_location,
    load_fourth_location,
    load_fifth_location,
    load_sixth_location,
    load_seventh_location,
    load_eighth_location,
    tree,
    movement_exchange,
    movement_detail,
    movement_list,
    show_instance_assembly_list,
)

urlpatterns = [
    path('search/', search_piece_database, name='search-piece-database'),
    path('search_instance/', search_instance_database, name='search-instance-database'),

    path('piece_list/', PieceListView.as_view(), name='piece'),
    path('piece_detail/<primary_key>', show_piece, name='piece-detail'),
    path('inventory/create/', PieceCreate.as_view(), name='piece-create'),
    path('update_piece/<piece_id>', update_piece, name='update-piece'),
    path('clone_piece/<piece_id>', clone_piece, name='piece-clone'),
    path('piece_history/<primary_key>', show_piece_history, name='piece-history'),


    path('piece_instance_list', all_piece_instance, name="piece-instance-list"),
    path('create_instance_piece/', PieceInstanceCreate.as_view(), name='piece-instance-create'),
    path('piece_instance_detail/<primary_key>', show_instance_form, name='piece-instance-detail'),
    path('delete_piece_instance/<instance_id>', delete_instance, name="delete-piece-instance"),
    path('update_piece_instance/<instance_id>', update_instance, name='update-piece-instance'),
    path('clone_existing_piece/<instance_id>', clone_instance, name='instance-clone'),
    path('instance_history/<primary_key>', show_instance_history, name='instance-history'),

    path('create_groupassembly/', GroupAssemblyCreate.as_view(), name='groupassembly-create'),
    path('groupassembly_list/', GroupAssemblyListView.as_view(), name='groupassembly-list'),
    path('groupassembly_detail/<primary_key>', show_groupassembly, name='groupassembly-detail'),
    path('kit_form/', KitCreate.as_view(), name='kit-create'),
    path('kit_list/', KitList.as_view(), name='kit-list'),
    path('kit_detail/<primary_key>', show_kit, name='kit-detail'),
    path('kit_update/<kit_id>', update_kit, name='kit-update'),
    path('computer_update/<kit_id>', update_computer_assembly, name='computer-update'),
    path('assembly_history/<primary_key>', show_assembly_history, name='assembly-history'),

    path('general_list', show_instance_assembly_list, name="assembly-instance-list"),

    path('database_csv', database_csv, name='database_csv'),

    path('movement_choice/', movement_exchange, name='movement-choice'),
    path('movement_detail/<primary_key>', movement_detail, name='movement-detail'),
    path('movement_list', movement_list, name="movement-list"),

    path('tree', tree, name='tree'),

    path('ajax/load-item_1/', load_item_1, name='ajax_load_item_1'),  # <-- this one here
    path('ajax/load-item_2/', load_item_2, name='ajax_load_item_2'),  # <-- this one here

    path('ajax/load-second_location/', load_second_location, name='ajax_load_second_location'),  # <-- this one here
    path('ajax/load-third_location/', load_third_location, name='ajax_load_third_location'),  # <-- this one here
    path('ajax/load-fourth_location/', load_fourth_location, name='ajax_load_fourth_location'),  # <-- this one here
    path('ajax/load-fifth_location/', load_fifth_location, name='ajax_load_fifth_location'),  # <-- this one here
    path('ajax/load-sixth_location/', load_sixth_location, name='ajax_load_sixth_location'),  # <-- this one here
    path('ajax/load-seventh_location/', load_seventh_location, name='ajax_load_seventh_location'),  # <-- this one here
    path('ajax/load-eighth_location/', load_eighth_location, name='ajax_load_eighth_location'),  # <-- this one here
]