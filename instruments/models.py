from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile
import urllib
from PIL import Image
import os
from instruments.base_models import *
import boto3
from django.conf import settings
import base64

class Instrument(BaseInstrument):
    pass


class Deployment(BaseDeployment):
    instrument = models.ForeignKey(
        Instrument, on_delete=models.CASCADE, blank=True, null=True)
    rows_from_start = models.IntegerField(default=0, blank=True, null=True)
    rows_from_end = models.IntegerField(default=None, blank=True, null=True)
    database_parameters = models.JSONField(default=dict, blank=True)

    def algolia_index(self):
        return {'imei': self.instrument.serial_number, 'instrument_name': self.instrument.name, 'instrument_type': self.instrument.instrument_type,  'details': self.instrument.details, 'avatar': self.instrument.avatar, 'is_simb3': self.instrument.is_simb3}

def custom_filename(instance, filename=None):
    """
    Function to generate a custom filename for the uploaded image.

    Written 19 Feb 2024
    """
    base_name, extension = os.path.splitext(filename)
    unique_full_filename = f"deployment/media/{instance.deployment.id}/{instance.uuid}{extension}"
   
    return unique_full_filename


class DeploymentMedia(models.Model):

    """
    Model for deployment media, like images, documents, etc. Uploads to 
    Amazon S3. 

    Written 19 Feb 2023
    """
    deployment = models.ForeignKey(Deployment, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.FileField(null=True, blank=True,
                                upload_to=custom_filename)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, null=True)
    private = models.BooleanField(blank=True, null=False, default=False)
    type = models.CharField(blank=True, null=True)
    size = models.CharField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

    def delete(self, *args, **kwargs):
        if self.location:
            self.location.delete(save=False)
        super(DeploymentMedia, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)        