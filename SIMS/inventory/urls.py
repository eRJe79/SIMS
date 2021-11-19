from django.urls import path

from .views import (
    ConsumableCreate, show_consumable, consumable_list, show_consumable_history, update_consumable, clone_consumable,
    PieceListView, PieceCreate, show_piece, update_piece, clone_piece, show_piece_history,
    PieceInstanceCreate, show_instance_form, delete_instance, update_instance, clone_instance, all_piece_instance,
    show_instance_history,
    search_consumable_database, search_piece_database, search_instance_database, search_groupassembly_database,
    search_assembly_database, search_general_database,  database_csv,
    GroupAssemblyCreate, GroupAssemblyListView, show_groupassembly,
    KitCreate, KitList, show_kit, update_kit, show_assembly_history,
    load_item_1, load_item_2, load_piece_kit,
    load_second_location, load_third_location, load_fourth_location, load_fifth_location, load_sixth_location,
    load_seventh_location, load_eighth_location,
    movement_exchange, movement_detail, movement_list, movement_revert,
    show_instance_assembly_list,
    create_equivalence, EquivalenceListView, equivalence_detail, update_equivalence,
    shipped_received_csv, movement_record_csv,  reparation_record_csv, low_stock_record_csv,
)

urlpatterns = [
    path('search_consumable/', search_consumable_database, name='search-consumable-database'),
    path('search/', search_piece_database, name='search-piece-database'),
    path('search_instance/', search_instance_database, name='search-instance-database'),
    path('search_groupassembly/', search_groupassembly_database, name='search-groupassembly-database'),
    path('search_assembly/', search_assembly_database, name='search-assembly-database'),
    path('search_general/', search_general_database, name='search-general-database'),

    path('consumable/create_consumable/', ConsumableCreate.as_view(), name='consumable-create'),
    path('consumable/consumable_detail/<primary_key>', show_consumable, name='consumable-detail'),
    path('consumable/consumable_list', consumable_list, name='consumable-list'),
    path('consumable/update_consumable/<consumable_id>', update_consumable, name='consumable-update'),
    path('consumable/clone_consumable/<consumable_id>', clone_consumable, name='consumable-clone'),
    path('consumable/consumable_history/<primary_key>', show_consumable_history, name='consumable-history'),

    path('piece/piece_list/', PieceListView.as_view(), name='piece'),
    path('piece/piece_detail/<primary_key>', show_piece, name='piece-detail'),
    path('piece/create/', PieceCreate.as_view(), name='piece-create'),
    path('piece/update_piece/<piece_id>', update_piece, name='update-piece'),
    path('piece/clone_piece/<piece_id>', clone_piece, name='piece-clone'),
    path('piece/piece_history/<primary_key>', show_piece_history, name='piece-history'),


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
    path('assembly/assembly_history/<primary_key>', show_assembly_history, name='assembly-history'),

    path('general_list', show_instance_assembly_list, name="assembly-instance-list"),

    # Reporting tool
    path('database_csv', database_csv, name='database_csv'),
    path('shipped_received_csv', shipped_received_csv, name='shipped_received_csv'),
    path('movement_record_csv', movement_record_csv, name='movement_record_csv'),
    path('reparation_record_csv', reparation_record_csv, name='reparation_record_csv'),
    path('low_stock_record_csv', low_stock_record_csv, name='low_stock_record_csv'),

    path('equivalence/create_equivalence/', create_equivalence, name='equivalence-create'),
    path('equivalence/equivalence_list/', EquivalenceListView.as_view(), name='equivalence-list'),
    path('equivalence/equivalence_detail/<primary_key>', equivalence_detail, name='equivalence-detail'),
    path('equivalence/equivalence_update/<equivalence_id>', update_equivalence, name='equivalence-update'),

    path('movement_choice/', movement_exchange, name='movement-choice'),
    path('movement_detail/<primary_key>', movement_detail, name='movement-detail'),
    path('movement_list', movement_list, name="movement-list"),
    path('movement_revert/<movement_id>', movement_revert, name='movement_revert'),

    path('ajax/load-item_1/', load_item_1, name='ajax_load_item_1'),
    path('ajax/load-item_2/', load_item_2, name='ajax_load_item_2'),

    path('ajax/load-piece_kit/', load_piece_kit, name='ajax_load_piece_kit'),

    path('ajax/load-second_location/', load_second_location, name='ajax_load_second_location'),
    path('ajax/load-third_location/', load_third_location, name='ajax_load_third_location'),
    path('ajax/load-fourth_location/', load_fourth_location, name='ajax_load_fourth_location'),
    path('ajax/load-fifth_location/', load_fifth_location, name='ajax_load_fifth_location'),
    path('ajax/load-sixth_location/', load_sixth_location, name='ajax_load_sixth_location'),
    path('ajax/load-seventh_location/', load_seventh_location, name='ajax_load_seventh_location'),
    path('ajax/load-eighth_location/', load_eighth_location, name='ajax_load_eighth_location'),
]