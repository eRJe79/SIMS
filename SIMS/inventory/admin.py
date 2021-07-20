from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    Piece, Kit
)
# This is to register the models in the admin website

class PieceInline(admin.TabularInline):
    model = Piece

@admin.register(Piece)
class PieceAdmin(SimpleHistoryAdmin):
    list_display = ('part_number', 'website', 'manufacturer', 'piece_model', 'manufacturer_serialnumber', 'description',
                    'documentation', 'item_type', 'item_characteristic', 'owner', 'restriction', 'history',
                    'cae_serial_number', 'kit', 'location', 'second_location', 'third_location', 'fourth_location',
                    'fifth_location', 'status')


@admin.register(Kit)
class KitAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'description')
    inlines = [PieceInline]
