from rest_framework import serializers

from articles.models import *


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['title', 'heading', 'image', 'slug']


class ArticleDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'
