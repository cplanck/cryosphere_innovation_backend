from rest_framework import serializers

from .models import *


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = '__all__'


class DeploymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deployment
        fields = '__all__'


class DeploymentInstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrument
        fields = ['name', 'avatar', 'id']


class DeploymentGETSerializer(serializers.ModelSerializer):
    instrument = DeploymentInstrumentSerializer()

    class Meta:
        model = Deployment
        fields = '__all__'
