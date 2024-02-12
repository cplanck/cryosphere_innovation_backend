import uuid

from django.contrib.auth.models import User
from django.db import models
from pyexpat import model


class UpdatesAndChanges(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    heading = models.CharField(max_length=200, blank=True, null=True)
    published = models.BooleanField(null=True, blank=True, default=False)
    body = models.TextField(max_length=5000, blank=True, null=True)
    published_date = models.DateField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title
    
class WebsiteStatus(models.Model):
    status = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.status


class CustomerQuote(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    requester_name = models.CharField(blank=True, null=True)
    requester_email = models.CharField(blank=True, null=True)
    details = models.JSONField(null=True, blank=True)
    product = models.CharField(max_length=200, blank=True, null=True)
    user_submitted = models.BooleanField(null=True, blank=True)
    quote_file = models.FileField(upload_to='quotes', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.details['name']


class Banner(models.Model):
    banner_text = models.CharField(blank=True, null=True)
    banner_link = models.CharField(blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.banner_text


class UserSurvey(models.Model):
    survey_num = models.IntegerField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.survey_num


class ContactUs(models.Model):
    subject = models.CharField(max_length=2000, blank=True, null=True)
    form_results = models.JSONField(null=True, blank=True)
    seen = models.BooleanField(blank=True, null=True, default=False)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.subject
