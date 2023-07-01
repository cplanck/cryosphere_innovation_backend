# from allauth.socialaccount.models import SocialAccount
from instruments.models import Deployment, Instrument
from rest_framework import serializers

from user_profiles.models import *
from user_profiles.models import UserProfile


class InstrumentSerialNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ['serial_number', 'avatar', 'instrument_type']


class DashboarDeploymentSerializer(serializers.ModelSerializer):
    instrument = InstrumentSerialNumberSerializer(read_only=True)

    class Meta:
        model = Deployment
        fields = ['name', 'id', 'status',
                  'deployment_start_date', 'deployment_end_date', 'instrument', 'data_uuid', 'location', 'path', 'slug']


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    dashboard_deployments = DashboarDeploymentSerializer(
        many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'full_name', 'avatar', 'social_login',
                  'has_social_avatar', 'dashboard_deployments', 'id']

    def get_avatar(self, obj):
        avatar = ''
        if obj.has_social_avatar:
            social_avatar = ''  # THIS NEEDS TO BE FIXED AS WE MOVE TO ONE-TAP LOGIN!
            if social_avatar:
                avatar = social_avatar
        elif obj.avatar:
            avatar = obj.avatar.url
        else:
            avatar = 'https://ui-avatars.com/api/?name=' + \
                obj.user.first_name + '+' + obj.user.last_name
        return avatar


class UserProfilePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'


class DashboardDeploymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['dashboard_deployments']
