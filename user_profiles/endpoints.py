import json
from os import stat

from authentication.http_cookie_authentication import CookieTokenAuthentication
from django.contrib.auth.models import User
from django.shortcuts import render
from instruments.deployment_permissions_filter import \
    deployment_permissions_filter
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import (IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from user_profiles.models import UserProfile
from user_profiles.serializers import *


class UserProfileEndpoint(viewsets.ModelViewSet):
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer
        else:
            return UserProfilePostSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class UserEndpoint(viewsets.ModelViewSet):
    """
    This endpoint is for admin use only. 
    """
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class DashboardDeploymentMigration(viewsets.ModelViewSet):

    """
    Temporary endpoint for moving "watched instruments" from the old
    system to the new system.
    """
    serializer_class = UserProfilePostSerializer
    queryset = UserProfile.objects.all()
    lookup_field = 'user'

    # def get_queryset(self):
    #     return UserProfile.objects.filter(user=self.request.data['user'])


class DashboardDeployments(viewsets.ModelViewSet):

    """
    Production endpoint for adding/removing deployments 
    from a users dashboard

    Note: dashboard_deployments in the request body must contain
    all deployments you wish to have on the field. A patch request
    will override them all.
    """

    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DashboardDeploymentSerializer
    queryset = UserProfile.objects.all()
    lookup_field = 'user'

    def partial_update(self, request, *args, **kwargs):
        profile = self.get_object()
        if 'add_deployment' in self.request.data:
            profile.dashboard_deployments.add(
                self.request.data['add_deployment'])
            return Response({'success': 'Deployment added'}, status=status.HTTP_201_CREATED)
        elif 'remove_deployment' in self.request.data:
            profile.dashboard_deployments.remove(
                self.request.data['remove_deployment'])
            return Response({'success': 'Deployment removed'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        user_profile = self.queryset.get(user=self.request.user)
        dashboard_deployments = deployment_permissions_filter(self,
                                                              user_profile.dashboard_deployments.all())
        serializer = DashboarDeploymentSerializer(
            dashboard_deployments, many=True)
        return Response(serializer.data)
