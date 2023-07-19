from django.contrib.auth.models import User
from django.db import models
from pyexpat import model


class UpdatesAndChanges(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    heading = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField(max_length=5000, blank=True, null=True)
    published_date = models.DateField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title


class CustomerQuote(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    requester_name = models.CharField(blank=True, null=True)
    requester_email = models.CharField(blank=True, null=True)
    details = models.JSONField(null=True, blank=True)
    product = models.CharField(max_length=200, blank=True, null=True)
    user_submitted = models.BooleanField(null=True, blank=True)
    quote_file = models.FileField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.details['name']
