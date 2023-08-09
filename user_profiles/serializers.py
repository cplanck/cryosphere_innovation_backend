# from allauth.socialaccount.models import SocialAccount
from dataclasses import field

from instruments.models import Deployment, Instrument
from rest_framework import serializers

from user_profiles.models import *
from user_profiles.models import UserProfile


class InstrumentSerialNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ['serial_number', 'avatar', 'instrument_type', 'name']


class DashboarDeploymentSerializer(serializers.ModelSerializer):
    instrument = InstrumentSerialNumberSerializer(read_only=True)

    class Meta:
        model = Deployment
        fields = ['name', 'id', 'status',
                  'deployment_start_date', 'deployment_end_date', 'instrument', 'data_uuid', 'location', 'path', 'slug']


class UserProfileSerializer(serializers.ModelSerializer):
    dashboard_deployments = DashboarDeploymentSerializer(
        many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'full_name', 'social_login',
                  'has_social_avatar', 'dashboard_deployments', 'id', 'beta_tester']


class UserSerializer(serializers.ModelSerializer):

    avatar = serializers.SerializerMethodField()
    beta_tester = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email',
                  'avatar', 'email', 'date_joined', 'is_staff', 'last_login', 'password', 'beta_tester']
        
    def get_avatar(self, obj):
        if obj.userprofile.avatar:
            return obj.userprofile.avatar.url
        if obj.userprofile.google_avatar:
            return obj.userprofile.google_avatar
        else:
            return f'https://api.dicebear.com/6.x/identicon/png?scale=70&seed={obj.userprofile.robot}'

    def get_beta_tester(self, obj):
        beta_tester = obj.userprofile.beta_tester
        return beta_tester


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserProfilePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'


class DashboardDeploymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['dashboard_deployments']
