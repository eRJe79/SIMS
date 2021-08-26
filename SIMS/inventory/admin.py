from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    Piece, PieceInstance, Kit, First_location, Second_location, Third_location
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
