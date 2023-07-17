from rest_framework import serializers

from articles.models import *


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'title', 'heading', 'status',
                  'image', 'slug', 'published_date']


class ArticleDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'


class ArticleImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleImages
        fields = '__all__'
