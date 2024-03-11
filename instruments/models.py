from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile
import urllib
from PIL import Image as PilImage, UnidentifiedImageError
import os
from instruments.base_models import *
from django.core.exceptions import ValidationError
import boto3
from django.conf import settings
import base64

class Instrument(BaseInstrument):
    pass


class Deployment(BaseDeployment):
    instrument = models.ForeignKey(
        Instrument, on_delete=models.CASCADE, blank=True, null=True)
    rows_from_start = models.IntegerField(default=0, blank=True, null=True)
    rows_from_end = models.IntegerField(default=0, blank=True, null=True)
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
    name = models.CharField(blank=True, null=True)
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

        if self.location and self.location.file.size > 20 * 1024 * 1024: 
            raise ValidationError("File size exceeds the limit of 50MB")
        
        super().save(*args, **kwargs)

        try:
            with self.location.open() as img_read:
                img = PilImage.open(img_read)
                img.verify()
                img.close()

                img = PilImage.open(img_read)

                max_size = 1500
                if img.height > img.width:
                    height_percent = (max_size / float(img.height))
                    width_size = int((float(img.width) * float(height_percent)))
                    new_size = (width_size, max_size)
                else:
                    width_percent = (max_size / float(img.width))
                    height_size = int((float(img.height) * float(width_percent)))
                    new_size = (max_size, height_size)

                if img.height > max_size or img.width > max_size:
                    img = img.resize(new_size, PilImage.ANTIALIAS)
                    img_temp = BytesIO()
                    image_format = 'PNG' if img.format is None else img.format
                    img.save(img_temp, format=image_format)
                    img_temp.seek(0)

                    self.location.save(
                        self.location.name,
                        content=ContentFile(img_temp.read()),
                        save=False
                    )
                    img_temp.close()

        except UnidentifiedImageError:
            pass

        super().save(*args, **kwargs)  # Save the model again to save the changes