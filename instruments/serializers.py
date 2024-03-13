from rest_framework import serializers
from user_profiles.serializers import UserSerializer, CollaboratorSerializer
from django.contrib.auth.models import User

from .models import *
from real_time_data.models import *


class SensorPackageInstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstrumentSensorPackage
        fields = ['id', 'template_name','template', 'time_stamp_field', 'time_stamp_format' , 'latitude_field', 'longitude_field', 'created_by_instrument_id', 'last_modified', 'date_added']

class DeploymentInstrumentOwnerSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar', 'id']
    
    def get_avatar(self, obj):
        if obj.userprofile.avatar:
            return obj.userprofile.avatar.url
        if obj.userprofile.google_avatar:
            return obj.userprofile.google_avatar
        else:
            return f'https://api.dicebear.com/6.x/identicon/png?scale=70&seed={obj.userprofile.robot}'


class InstrumentSerializer(serializers.ModelSerializer):

    deployment_num = serializers.SerializerMethodField()

    class Meta:
        model = Instrument
        fields = '__all__'
        # fields = ['name', 'serial_number', 'sensor_package', 'unique_index', 'owner', 'avatar', 'deployment_num']
        # read_only_fields = ['name', 'serial_number', 'sensor_package', 'unique_index', 'owner', 'avatar', 'owner', 'sensor_package']


    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if request and request.method == 'GET':
            fields['owner'] = UserSerializer()
            fields['sensor_package'] = SensorPackageInstrumentSerializer()
        return fields
    
    
    def get_deployment_num(self, obj):
        return Deployment.objects.filter(instrument=obj).count()


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
        fields = ['name', 'avatar', 'id', 'owner',
                  'serial_number', 'instrument_type', 'sensor_package', 'is_simb3', 'unique_index', 'notes', 'build_date', 'notes', 'description', 'organization']
        read_only_fields=fields

class DeploymentGETSerializer(serializers.ModelSerializer):
    """
    Returns a nested representation of instrument on GET requests
    # """
    instrument = DeploymentInstrumentSerializer()
    collaborators = CollaboratorSerializer(many=True)
    real_time_data = serializers.SerializerMethodField(method_name='get_real_time_data')

    def get_real_time_data(self, deployment):
            real_time_data_instances = RealTimeData.objects.filter(deployment=deployment)
            serializer = RealTimeDataSnippetSerializer(real_time_data_instances, many=True)
            return serializer.data
    
    class Meta:
        model = Deployment
        fields = '__all__'
        read_only_fields = ['instrument', 'collaborators', 'real_time_data', 'owner', 'deployment_number', 'name', 'status', 'location', 'path', 'data_uuid', 'deployment_description', 'deployment_start_date', 'deployment_end_date', 'collaborators']

class PublicDeploymentGETSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deployment
        fields = ['name', 'status', 'location', 'slug', 'data_uuid', 'deployment_description', 'deployment_notes', 'deployment_start_date', 'deployment_end_date', 'details']

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

class DeploymentMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeploymentMedia
        fields = '__all__'