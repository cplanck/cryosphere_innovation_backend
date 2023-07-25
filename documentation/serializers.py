from rest_framework import serializers

from documentation.models import *


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ['id', 'title', 'heading', 'status',
                  'image', 'slug', 'published_date']


class DocumentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = '__all__'


class DocumentImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentImages
        fields = '__all__'
