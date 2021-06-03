from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_admin', 'is_main_user', 'is_lambda']


admin.site.register(User, UserAdmin)
