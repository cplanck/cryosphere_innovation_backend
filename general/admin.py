from django.contrib import admin

from .models import CustomerQuote, UpdatesAndChanges

admin.site.register(UpdatesAndChanges)
admin.site.register(CustomerQuote)
