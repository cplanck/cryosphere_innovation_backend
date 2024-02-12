from rest_framework import serializers
from .models import DeploymentDownload
from user_profiles.models import UserProfile
from instruments.models import Deployment
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar']

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        if obj.google_avatar:
            return obj.google_avatar
        else:
            return f'https://api.dicebear.com/6.x/identicon/png?scale=50&seed={obj.robot}'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class DeploymentDownloadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    avatar = serializers.SerializerMethodField()
    deployment = serializers.SerializerMethodField()

    class Meta:
        model = DeploymentDownload
        fields = '__all__'

    def get_avatar(self, obj):
        try:
            return UserProfileSerializer().get_avatar(obj.user.userprofile)
        except:
            return  f'https://api.dicebear.com/6.x/identicon/png?scale=50&seed=Snickers'
    
    def get_deployment(self, obj):
        return {'id': obj.deployment.id, 'name': obj.deployment.name, 'slug': obj.deployment.slug, 'status': obj.deployment.status}
        
    
class DeploymentDownloadPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeploymentDownload
        fields = '__all__'
