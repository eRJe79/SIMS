from django.contrib import admin

from .models import (
    Category, Location, Piece, PieceInstance
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('part_number', 'website', 'manufacturer')
    fields = ['part_number', 'website', 'manufacturer']

class PieceInstanceInline(admin.TabularInline):
    model = PieceInstance

@admin.register(Piece)
class PieceAdmin(admin.ModelAdmin):
    list_display = ('piece_model', 'cae_serialnumber', 'display_category', 'description', 'documentation', 'item_type', 'item_characteristic')
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
