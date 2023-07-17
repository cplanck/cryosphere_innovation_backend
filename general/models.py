from django.db import models


class UpdatesAndChanges(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    heading = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField(max_length=5000, blank=True, null=True)
    published_date = models.DateField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title
