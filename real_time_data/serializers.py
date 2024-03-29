from rest_framework import serializers
from .models import RealTimeData, DecodeScript, SBDData

class RealTimeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealTimeData
        fields = '__all__'
        depth = 2

class RealTimeDataPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealTimeData
        fields = ['deployment', 'active', 'iridium_sbd', 'iridium_imei', 'decode_script', 'id', 'updated', 'resyncing', 'downloading']

class DecodeScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecodeScript
        fields = '__all__'

class GetSBDDetailsByDeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SBDData
        fields = ['sbd_filename', 'last_modified']
