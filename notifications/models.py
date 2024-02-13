from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):

    for_user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user', blank=True, null=True)
    type = models.CharField(null=True, blank=True)
    content = models.JSONField(null=True, blank=True)
    seen = models.BooleanField(null=True, blank=True, default=False)
    read = models.BooleanField(null=True, blank=True, default=False)
    deleted = models.BooleanField(null=True, blank=True, default=False)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)


    def __str__(self):
        return f'{self.for_user} notification'
