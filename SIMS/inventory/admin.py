from django.contrib import admin

from .models import (
    Article,
    Item
)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['manufacturer',
                  'manufacturer_partnumber',
                  #'manufacturer_serienumber',
                  #'website',
                  'contractor',
                  'contractor_partnumber',
                  #'contractor_serienumber',
                  ]

class ItemAdmin(admin.ModelAdmin):
    list_display = ['article_related',
                  'cae_partname',
                  #'CAEPartNumber',
                  #'CAESerialNumber',
                  'item_model']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Item, ItemAdmin)
