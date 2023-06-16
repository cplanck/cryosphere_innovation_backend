import secrets

from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string


class APIKey(models.Model):

    def generate_key():
        return get_random_string(length=32)

    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    permissions = models.JSONField(blank=True, null=True)
    key = models.CharField(max_length=64, unique=True, default=generate_key)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key
