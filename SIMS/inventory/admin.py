from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from treenode.admin import TreeNodeModelAdmin
from treenode.forms import TreeNodeForm

from .models import (
    Piece, PieceInstance, Kit, LocationCheck,
    First_location, Second_location, Third_location, Fourth_location,
    Fifth_location, Sixth_location, Seventh_location, Eighth_location,
)
# This is to register the models in the admin website

class PieceInstanceInline(admin.TabularInline):
    model = PieceInstance

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
    list_display = ('name',)

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

@admin.register(LocationCheck)
class LocationCheckAdmin(TreeNodeModelAdmin):
    list_display = ('location_name',)
    treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
    # treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_BREADCRUMBS
    # treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_INDENTATION

    # use TreeNodeForm to automatically exclude invalid parent choices
    form = TreeNodeForm


@admin.register(Piece)
class PieceAdmin(SimpleHistoryAdmin):
    list_display = ('website', 'manufacturer', 'manufacturer_part_number', 'piece_model', 'description', 'documentation', 'item_type', 'item_characteristic',)
    inlines = [PieceInstanceInline]

@admin.register(PieceInstance)
class PieceInstanceAdmin(SimpleHistoryAdmin):
    list_display = ('serial_number', 'piece', 'kit', 'manufacturer_serialnumber', 'owner', 'restriction', 'first_location', 'second_location', 'third_location', 'fourth_location', 'fifth_location', 'status', 'history')

@admin.register(Kit)
class KitAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'description')
    inlines = [PieceInstanceInline]
