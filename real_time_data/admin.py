from django.contrib import admin
from .models import RealTimeData, DecodeScript

class RealTimeDataAdmin(admin.ModelAdmin):
    list_display = ['deployment', 'active', 'decode_script', 'iridium_imei']


admin.site.register(RealTimeData, RealTimeDataAdmin)
admin.site.register(DecodeScript)
