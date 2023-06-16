from django.contrib import admin

from .models import *


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ['key', 'user', 'active']


admin.site.register(APIKey, ApiKeyAdmin)
