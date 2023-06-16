import uuid
from contextlib import nullcontext

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ImageField


class BaseInstrument(models.Model):

    """
    Main instrument base class. This class is not directly instantiated but
    provides the standard attributes used in subsequent classes. 
    """

    name = models.CharField(max_length=200, null=True)
    serial_number = models.CharField(max_length=100, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    notes = models.TextField(max_length=5000, null=True, blank=True)
    details = models.JSONField(blank=True, null=True)
    instrument_type = models.CharField(max_length=200, null=True, blank=True)
    internal = models.BooleanField(default=False)
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
    starred = models.BooleanField(default=False, null=True, blank=True)
    starred_date = models.DateTimeField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
