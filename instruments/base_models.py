import uuid
from contextlib import nullcontext
from tabnanny import verbose

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ImageField


class InstrumentSensorPackage(models.Model):
    """
    Instrument sensor package class. 
    Used to define an instruments sensor package so that plots can
    be created for the frontend.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    fields = models.JSONField(
        default=dict, blank=True, null=True)
    template = models.BooleanField(blank=True, null=True)
    template_name = models.TextField(max_length=100, null=True, blank=True)
    time_stamp_field = models.JSONField(default=dict, blank=True, null=True)
    latitude_field = models.JSONField(default=dict, blank=True, null=True)
    longitude_field = models.JSONField(default=dict, blank=True, null=True)
    time_stamp_format = models.TextField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.template_name or 'generic'

    class Meta:
        verbose_name = 'Instrument Sensor Package'

def generate_instrument_avatar_upload_path(instance, filename):
    return f'instruments/avatars/{instance.id}/{filename}'

class BaseInstrument(models.Model):

    """
    Main instrument base class. This class is not directly instantiated but
    provides the standard attributes used in subsequent classes. 
    """

    def get_image_upload_path(instance, filename):
        """This is unused but breaks migrations if deleted"""
        pass 

    name = models.CharField(max_length=200, null=True)
    serial_number = models.CharField(max_length=100, null=True)
    sensor_package = models.ForeignKey(
        InstrumentSensorPackage, on_delete=models.SET_NULL, blank=True, null=True)
    sensors = models.JSONField(default=dict, blank=True, null=True)
    unique_index = models.CharField(null=True, blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    avatar = models.ImageField(
        upload_to=generate_instrument_avatar_upload_path, null=True, blank=True)
    is_simb3 = models.BooleanField(null=True, blank=True, default=False)
    description = models.TextField(max_length=2000, null=True, blank=True)
    notes = models.TextField(max_length=5000, null=True, blank=True)
    details = models.JSONField(blank=True, null=True)
    instrument_type = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class BaseDeployment(models.Model):

    """
    Deployment base class. This class is not directly instantiated but 
    provides the standard attributes used in subsequent classeses.
    """

    deployment_number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True)
    path = models.CharField(max_length=500, null=True, blank=True)
    slug = models.CharField(max_length=500, null=True, blank=True, unique=True)
    data_uuid = models.UUIDField(default=uuid.uuid4, editable=True)
    deployment_description = models.TextField(
        max_length=2000, null=True, blank=True)
    deployment_notes = models.TextField(max_length=5000, null=True, blank=True)
    deployment_start_date = models.DateTimeField(null=True, blank=True)
    deployment_end_date = models.DateTimeField(null=True, blank=True)
    private = models.BooleanField(default=False, null=True, blank=True)
    details = models.JSONField(blank=True, null=True)
    collaborators = models.ManyToManyField(
        User, related_name='collaborators', blank=True)
    searchable = models.BooleanField(blank=True, null=True, default=False)
    web_page_enabled = models.BooleanField(default=False, null=True, blank=True)
    unique_index = models.CharField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


