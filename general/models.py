from django.db import models
from pyexpat import model

# Create your models here.


class UpdatesAndChanges(models.Model):
    heading = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField(max_length=5000, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
