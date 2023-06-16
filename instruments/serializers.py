from rest_framework import serializers

from .models import *


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = '__all__'


class DeploymentInstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrument
        fields = ['name', 'avatar', 'id',
                  'serial_number', 'instrument_type']


class DeploymentGETSerializer(serializers.ModelSerializer):
    """
    Returns a nested representation of instrument on GET requests
    """
    instrument = DeploymentInstrumentSerializer()

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
