from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    Piece, PieceInstance
)
# This is to register the models in the admin website

class PieceInstanceInline(admin.TabularInline):
    model = PieceInstance

@admin.register(Piece)
class PieceAdmin(SimpleHistoryAdmin):
    list_display = ('part_number', 'website', 'manufacturer', 'piece_model', 'manufacturer_serialnumber', 'description', 'documentation', 'item_type', 'item_characteristic', 'owner', 'restriction')
    inlines = [PieceInstanceInline]

@admin.register(PieceInstance)
class PieceInstanceAdmin(SimpleHistoryAdmin):
    list_display = ('serial_number', 'piece', 'location', 'second_location', 'third_location', 'fourth_location', 'fifth_location', 'status', 'history')
