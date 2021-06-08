from django.contrib import admin

from .models import (
    Piece, PieceInstance
)


class PieceInstanceInline(admin.TabularInline):
    model = PieceInstance

@admin.register(Piece)
class PieceAdmin(admin.ModelAdmin):
    list_display = ('part_number', 'website', 'manufacturer', 'piece_model', 'cae_serialnumber', 'description', 'documentation', 'item_type', 'item_characteristic')
    inlines = [PieceInstanceInline]

@admin.register(PieceInstance)
class PieceInstanceAdmin(admin.ModelAdmin):
    list_display = ('piece', 'id', 'location', 'status', 'display_piece', 'owner', 'restriction')
    list_filter = ('location', 'status')
    fieldsets = (
        (None, {
            'fields': ('piece', 'id')
        }),
        ('Specification', {
            'fields': ('status', 'location', 'owner', 'restriction')
        }),
    )
