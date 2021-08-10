from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    Piece, PieceInstance, Kit
)
# This is to register the models in the admin website

class PieceInstanceInline(admin.TabularInline):
    model = PieceInstance

@admin.register(Piece)
class PieceAdmin(SimpleHistoryAdmin):
    list_display = ('website', 'manufacturer', 'piece_model', 'description', 'documentation', 'item_type', 'item_characteristic',)
    inlines = [PieceInstanceInline]

@admin.register(PieceInstance)
class PieceInstanceAdmin(SimpleHistoryAdmin):
    list_display = ('serial_number', 'piece', 'kit','part_number', 'manufacturer_serialnumber', 'owner', 'restriction', 'location', 'second_location', 'third_location', 'fourth_location', 'fifth_location', 'status', 'history')

@admin.register(Kit)
class KitAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'description')
    inlines = [PieceInstanceInline]
