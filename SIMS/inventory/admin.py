from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Piece, PieceInstance, Kit, GroupAssembly, MovementExchange, Equivalence,
    First_location, Second_location, Third_location, Fourth_location,
    Fifth_location, Sixth_location, Seventh_location, Eighth_location,
)


# This is to register the models in the admin website
class PieceInstanceInline(admin.TabularInline):
    model = PieceInstance


class KitInline(admin.TabularInline):
    model = Kit


class PieceAdminInline(admin.TabularInline):
    model = Piece


@admin.register(First_location)
class First_locationAdmin(SimpleHistoryAdmin):
    list_display = ('name',)


@admin.register(Second_location)
class Second_LocationAdmin(SimpleHistoryAdmin):
    list_display = ('previous_loc', 'name')


@admin.register(Third_location)
class Third_LocationAdmin(SimpleHistoryAdmin):
    list_display = ('previous_loc', 'name')


@admin.register(Fourth_location)
class Fourth_locationAdmin(SimpleHistoryAdmin):
    list_display = ('previous_loc', 'name')


@admin.register(Fifth_location)
class Fifth_LocationAdmin(SimpleHistoryAdmin):
    list_display = ('previous_loc', 'name')


@admin.register(Sixth_location)
class Sixth_LocationAdmin(SimpleHistoryAdmin):
    list_display = ('previous_loc', 'name')


@admin.register(Seventh_location)
class Feventh_LocationAdmin(SimpleHistoryAdmin):
    list_display = ('previous_loc', 'name')


@admin.register(Eighth_location)
class Eighth_LocationAdmin(SimpleHistoryAdmin):
    list_display = ('previous_loc', 'name')


@admin.register(Equivalence)
class EquivalenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'pieceeq_1', 'pieceeq_2', 'pieceeq_3', 'pieceeq_4', 'pieceeq_5', 'pieceeq_6',
    'pieceeq_7', 'pieceeq_8', 'pieceeq_9', 'pieceeq_10', 'pieceeq_11', 'pieceeq_12', 'pieceeq_13', 'pieceeq_14', 'pieceeq_15')


@admin.register(Piece)
class PieceAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ('name', 'website', 'manufacturer', 'manufacturer_part_number', 'piece_model', 'description',
                    'documentation', 'item_type', 'item_characteristic',)
    inlines = [PieceInstanceInline]


@admin.register(PieceInstance)
class PieceInstanceAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ('serial_number', 'piece', 'manufacturer_serialnumber', 'provider_serialnumber', 'owner',
                    'restriction', 'update_document', 'update_comment', 'date_update',
                    'date_calibration', 'date_created', 'date_guarantee', 'date_end_of_life',
                    'first_location', 'second_location', 'third_location', 'fourth_location', 'fifth_location',
                    'sixth_location', 'seventh_location', 'eighth_location',
                    'status', 'history')


@admin.register(Kit)
class KitAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'kit_serialnumber', 'group_assembly', 'description', 'kit_serialnumber',
                    'manufacturer_serialnumber', 'provider_serialnumber', 'kit_status', 'pn_1', 'pn_2', 'pn_3', 'pn_4',
                    'pn_5', 'pn_6', 'pn_7', 'pn_8', 'pn_9', 'pn_10', 'pn_11', 'pn_12', 'pn_13', 'pn_14', 'pn_15',
                    'piece_kit_1', 'piece_kit_2', 'piece_kit_3', 'piece_kit_4', 'piece_kit_5', 'piece_kit_6',
                    'piece_kit_7', 'piece_kit_8', 'piece_kit_9', 'piece_kit_10', 'piece_kit_11', 'piece_kit_12',
                    'piece_kit_13', 'piece_kit_14', 'piece_kit_15', 'first_location', 'second_location', 'third_location',
                    'fourth_location', 'fifth_location', 'sixth_location', 'seventh_location', 'eighth_location',
                    'update_comment')


@admin.register(GroupAssembly)
class GroupAssemblyAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'kit_partnumber')
    inlines = [KitInline]


@admin.register(MovementExchange)
class MovementExchangeAdmin(SimpleHistoryAdmin):
    list_display = ('piece_1', 'piece_2', 'item_1', 'item_2', 'reference_number')


