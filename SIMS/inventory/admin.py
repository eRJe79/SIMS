from django.contrib import admin

from .models import (
    Item
)

class ItemAdmin(admin.ModelAdmin):
    list_display = ['manufacturer',
                  #'manufacturer_partnumber',
                  #'manufacturer_serienumber',
                  'manufacturer_date',
                  'website',
                  'contractor',
                  #'contractor_partnumber',
                  #'contractor_serienumber',
                  #'part_number',
                  'cae_partname',
                  #'CAEPartNumber',
                  #'CAESerialNumber',
                  'item_model']


admin.site.register(Item, ItemAdmin)
