from tokenize import blank_re

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Article_tags(models.Model):
    tag_name = models.CharField(max_length=100, null=True, blank=True)
    tag_color = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = 'Article Tag'
        verbose_name_plural = 'Article Tags'

    def __str__(self):
        return self.tag_name


class ArticleImages(models.Model):
    location = models.ImageField(null=True, blank=True,
                                 upload_to='articles/images')
    article_id = models.IntegerField(null=True, blank=True)


class Article(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=500, null=True, blank=True)
    path = models.CharField(max_length=500, null=True, blank=True)
    status_choices = [('Draft', 'Draft'), ('Published', 'Published'),
                      ('Archived', 'Archived'), ('Internal', 'Internal')]
    status = models.CharField(choices=status_choices,
                              default='Draft', max_length=30)
    internal = models.BooleanField(default=False)
    heading = models.CharField(max_length=500, null=True, blank=True)
    featured = models.BooleanField(null=True, blank=True, default=0)
    featured_heading = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(null=True, blank=True,
                              upload_to='article_images')
    image_attribution = models.CharField(max_length=500, null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    updated_date = models.DateField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title


class Author(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, to_field='username')
    display_name = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Authors'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.display_name
