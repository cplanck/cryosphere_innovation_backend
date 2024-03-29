from django.db import models
from instruments.models import Deployment


class DecodeScript(models.Model):
    name = models.CharField(blank=True, null=True)
    script = models.TextField( blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class RealTimeData(models.Model):
    deployment = models.OneToOneField(Deployment, on_delete=models.CASCADE, blank=True)
    active = models.BooleanField(default=False, blank=True)
    iridium_sbd = models.BooleanField(default=True, null=True, blank=True)
    iridium_imei = models.CharField(null=True, blank=True)
    decode_script = models.ForeignKey(DecodeScript, null=True, on_delete=models.SET_NULL, blank=True)
    downloading = models.BooleanField(blank=True, null=True, default=False)
    resyncing = models.BooleanField(blank=True, null=True, default=False)
    error = models.CharField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.deployment.name
    
    class Meta:
        verbose_name = 'Real-Time Data'
        verbose_name_plural = 'Real-Time Data'

class SBDData(models.Model):
    deployment = models.ForeignKey(Deployment, on_delete=models.SET_NULL, blank=True, null=True)
    sbd_binary = models.BinaryField()
    sbd_filename = models.CharField(null=True, blank=True, unique=True)
    gmail_message_id = models.CharField(null=True, blank=True, unique=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)