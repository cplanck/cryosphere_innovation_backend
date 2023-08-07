from django.db import models

from instruments.base_models import *


class Instrument(BaseInstrument):
    pass


class Deployment(BaseDeployment):
    instrument = models.ForeignKey(
        Instrument, on_delete=models.CASCADE, blank=True, null=True)
    rows_from_start = models.IntegerField(default=0, blank=True, null=True)
    rows_from_end = models.IntegerField(default=None, blank=True, null=True)

    def algolia_index(self):
        return {'imei': self.instrument.serial_number, 'instrument_name': self.instrument.name, 'instrument_type': self.instrument.instrument_type,  'details': self.instrument.details, 'avatar': self.instrument.avatar}

# class RealTimeDecoding(models.Model):
#     deployment = models.OneToOneField(Deployment, on_delete=models.CASCADE)
#     active = models.BooleanField(default=False)
#     decode_script_name = models.CharField(blank=True, null=True)
#     date_added = models.DateTimeField(auto_now_add=True, null=True)
#     last_modified = models.DateTimeField(auto_now=True, null=True)

#     def __str__(self):
#         return self.deployment.name
    
#     class Meta:
#         verbose_name = 'Real-Time Data'
