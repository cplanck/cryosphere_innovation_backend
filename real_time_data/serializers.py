from rest_framework import serializers
from .models import RealTimeData, DecodeScript

class RealTimeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealTimeData
        fields = '__all__'
        depth = 2

class DecodeScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecodeScript
        fields = '__all__'
