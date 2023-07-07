from rest_framework import serializers
from user_profiles.serializers import UserSerializer

from .models import *


class SensorPackageInstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstrumentSensorPackage
        fields = ['id', 'name']


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


class DeploymentInstrumentSerializer(serializers.ModelSerializer):
    sensor_package = SensorPackageInstrumentSerializer()

    class Meta:
        model = Instrument
        fields = ['name', 'avatar', 'id',
                  'serial_number', 'instrument_type', 'sensor_package']


class DeploymentGETSerializer(serializers.ModelSerializer):
    """
    Returns a nested representation of instrument on GET requests
    """
    instrument = DeploymentInstrumentSerializer()
    collaborators = UserSerializer(many=True)

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
