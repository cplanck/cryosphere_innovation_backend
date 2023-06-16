from django.contrib import admin

from .models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured']


admin.site.register(Article, ArticleAdmin)
