from rest_framework import serializers
from user_profiles.serializers import UserSerializer
from django.contrib.auth.models import User

from .models import *
from real_time_data.models import *


class SensorPackageInstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstrumentSensorPackage
        fields = ['id', 'name']

class DeploymentInstrumentOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class InstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrument
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if request and request.method == 'GET':
            fields['owner'] = UserSerializer()
            fields['sensor_package'] = SensorPackageInstrumentSerializer()
        return fields


class InstrumentPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = '__all__'

class RealTimeDataSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealTimeData
        fields = ['active', 'iridium_sbd', 'updated', 'error']

class DeploymentInstrumentSerializer(serializers.ModelSerializer):
    sensor_package = SensorPackageInstrumentSerializer()
    owner = DeploymentInstrumentOwnerSerializer()

    class Meta:
        model = Instrument
        fields = ['name', 'avatar', 'id',
                  'serial_number', 'instrument_type', 'sensor_package', 'owner']


class DeploymentGETSerializer(serializers.ModelSerializer):
    """
    Returns a nested representation of instrument on GET requests
    """
    instrument = DeploymentInstrumentSerializer()
    collaborators = UserSerializer(many=True)
    real_time_data = serializers.SerializerMethodField(method_name='get_real_time_data')

    def get_real_time_data(self, deployment):
            real_time_data_instances = RealTimeData.objects.filter(deployment=deployment)
            serializer = RealTimeDataSnippetSerializer(real_time_data_instances, many=True)
            return serializer.data
    
    class Meta:
        model = Deployment
        fields = '__all__'


class DeploymentSerializer(serializers.ModelSerializer):
    """
    Used for POST/PATCH requests (all other than GET) and 
    requires on an instrument_id to instantiate. 
    """
    class Meta:
        model = Deployment
        fields = '__all__'


class InstrumentSensorPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentSensorPackage
        fields = '__all__'
