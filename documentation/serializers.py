from rest_framework import serializers

from documentation.models import *


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ['id', 'title', 'heading', 'status',
                  'image', 'slug', 'published_date', 'type', 'category']


class DocumentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = '__all__'


class DocumentMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentMedia
        fields = '__all__'
