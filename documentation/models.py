import os
import uuid
from tokenize import blank_re

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Document_tags(models.Model):
    tag_name = models.CharField(max_length=100, null=True, blank=True)
    tag_color = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = 'Documentation Tag'
        verbose_name_plural = 'Documentation Tags'

    def __str__(self):
        return self.tag_name


def custom_filename(instance, filename):
    """
    Function to generate a custom filename for the uploaded image.
    """
    unique_filename = f"documentation/media/{uuid.uuid4()}_{filename}"
    return unique_filename


class DocumentMedia(models.Model):
    location = models.FileField(null=True, blank=True,
                                upload_to=custom_filename)
    type = models.CharField(blank=True, null=True)
    size = models.CharField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def delete(self, *args, **kwargs):
        if self.location:
            self.location.delete(save=False)
        super(DocumentMedia, self).delete(*args, **kwargs)


class Document(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(choices=[('Doc', 'Doc'), ('Article', 'Article')],
                            default='Doc', max_length=30)
    slug = models.SlugField(max_length=500, null=True, blank=True)
    path = models.CharField(max_length=500, null=True, blank=True)
    status_choices = [('Draft', 'Draft'), ('Published', 'Published'),
                      ('Archived', 'Archived'), ('Internal', 'Internal')]
    status = models.CharField(choices=status_choices,
                              default='Draft', max_length=30)
    internal = models.BooleanField(default=False)
    heading = models.CharField(max_length=500, null=True, blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(null=True, blank=True,
                              upload_to='documentation/images')
    image_attribution = models.CharField(max_length=500, null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    updated_date = models.DateField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Documentation'
        verbose_name_plural = 'Documentation'

    def __str__(self):
        return self.title
