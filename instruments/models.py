from django.db import models

from instruments.base_models import *


class Instrument(BaseInstrument):
    pass


class Deployment(BaseDeployment):
    instrument = models.ForeignKey(
        Instrument, on_delete=models.CASCADE, blank=True, null=True)

    def algolia_index(self):
        return {'imei': self.instrument.serial_number, 'instrument_name': self.instrument.name, 'instrument_type': self.instrument.instrument_type,  'details': self.instrument.details, 'avatar': self.instrument.avatar}
