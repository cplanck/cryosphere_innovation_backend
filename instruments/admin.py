from django.contrib import admin

from .models import *


class InstrumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_number', 'instrument_type']


class DeploymentAdmin(admin.ModelAdmin):
    filter_horizontal = ('collaborators',)
    list_display = ['name', 'instrument',
                    'deployment_number', 'status', 'private']


admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Deployment, DeploymentAdmin)
