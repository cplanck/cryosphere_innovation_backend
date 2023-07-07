import json
import re
import uuid
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


class UserSettingsEndpoint(viewsets.ModelViewSet):
    """
    Production endpoint for modifying user settings from 
    the user dashboard.
    Note: this endpoint is a little more complicated because 
    it modifies two models, User and UserProfile.
    """

    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def partial_update(self, request, *args, **kwargs):
        request.data._mutable = True
        user = self.get_object()
        user_profile = UserProfile.objects.get(user=user)

        if 'avatar' in request.data:
            avatar = request.data['avatar']
            file_type = avatar.content_type.split('/')[1]
            request.data.pop('avatar')
            user_profile.avatar.save(
                f"{user.id}/{uuid.uuid4()}.{file_type})", avatar)

        email = request.data['email']
        print(email)
        # check if email exists
        if self.queryset.filter(email=email).exists() and user.email != email:
            print(
                f'EMAIL {email} ALREADY EXISTS. SELECT A NEW ONE (YOUR CURRENT EMAIL IS {user.email}')
            return Response({'email': 'exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            res = {'email': serializer.data['email'], 'first_name': serializer.data['first_name'],
                   'last_name': serializer.data['last_name']}
            # print(user_profile.avatar.)
            if user_profile.avatar:
                res['avatar'] = user_profile.avatar.url
            return Response(res, status=status.HTTP_200_OK)


class UserProfileEndpoint(viewsets.ModelViewSet):

    """
    Get the user profile for a logged in user. 
    """
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
    This endpoint is for admin use only. It returns all user objects in the database. 
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
