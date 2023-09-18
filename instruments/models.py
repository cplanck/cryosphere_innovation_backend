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
        return {'imei': self.instrument.serial_number, 'instrument_name': self.instrument.name, 'instrument_type': self.instrument.instrument_type,  'details': self.instrument.details, 'avatar': self.instrument.avatar, 'is_simb3': self.instrument.is_simb3}
