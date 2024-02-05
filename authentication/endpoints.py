import json
import os
import random
import re
import urllib.parse
import uuid
from datetime import datetime, timedelta
from random import seed

import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from dotenv import load_dotenv
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import pagination, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)
from user_profiles.models import UserProfile
import datetime
from user_profiles.serializers import UserProfileSerializer

from authentication.http_cookie_authentication import CookieTokenAuthentication

from .models import APIKey
from .serializers import *

load_dotenv()


def prepare_user_response(user, avatar):
    """
    If user is authenticated, prepare their response. 
    """
    user_profile = UserProfile.objects.get(user=user)

    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token

    response = JsonResponse(
        {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_staff': user.is_staff,
            'avatar': avatar,
            'profile': UserProfileSerializer(user_profile).data
        })

    response.set_cookie('access_token', str(
        access_token), 
        httponly=True, 
        samesite='None', 
        secure=True, 
        domain=os.environ['COOKIE_DOMAIN'],
        expires=datetime.utcnow() + timedelta(days=30)
        )
    response.set_cookie('refresh_token', str(
        refresh_token), 
        httponly=True, 
        samesite='None', 
        secure=True, 
        domain=os.environ['COOKIE_DOMAIN'],
        expires=datetime.utcnow() + timedelta(days=30))

    return response


class GoogleOneTap(APIView):

    def post(self, request):
        try:
            user_info_from_google = id_token.verify_oauth2_token(
                request.data, requests.Request(), os.environ['GOOGLE_CLIENT_ID'])

            user = User.objects.filter(email=user_info_from_google['email'])

            if user:
                try:
                    # check if user has uploaded avatar
                    user = user.first()
                    user_profile = UserProfile.objects.get(user=user)
                    if user_profile.avatar:
                        avatar = user_profile.avatar.url
                    else:
                        # this will cause an error if it doesn't exist
                        avatar = user_info_from_google['picture']
                        user_profile.google_avatar = avatar
                        user_profile.save()
                except:
                    avatar = f'https://api.dicebear.com/6.x/identicon/png?scale=70&seed={user_profile.robot}'

                login(
                    request, user, backend='authentication.email_authentication_backend.EmailBackend')
                response = prepare_user_response(user, avatar)

                return response
            else:
                # User email doesn't exist in system, so create the user
                user = User.objects.create_user(
                    username=uuid.uuid4(), email=user_info_from_google['email'])
                user.set_unusable_password()

                user_profile = UserProfile.objects.get(user=user)

                dice_bear_avatar = ['Maggie', 'Mittens', '  ',
                                 'Pumpkin', 'Peanut', 'Socks', 'Jasmine', 'Snickers']
                user_profile.robot = random.choice(dice_bear_avatar)
                user_profile.social_login = True

                try:
                    avatar = user_info_from_google['picture']
                    user_profile.google_avatar = avatar
                except:
                    avatar = f'https://api.dicebear.com/6.x/identicon/png?scale=70&seed={user_profile.robot}'
                    user_profile.google_avatar = None

                user_profile.save()

                try:
                    if user_info_from_google['given_name']:
                        user.first_name = user_info_from_google['given_name']
                except:
                    user.first_name = 'no_given_name'
                try:
                    if user_info_from_google['family_name']:
                        user.last_name = user_info_from_google['family_name']
                except:
                    user.first_name = 'no_family_name'

                user.save()
                login(
                    request, user, backend='authentication.email_authentication_backend.EmailBackend')
                response = prepare_user_response(user, avatar)
                return response

        except Exception as e:
            print(e)
            return HttpResponse({'There was a problem logging you in'})


class StandardLogin(APIView):

    """
    Custom endpoint for returning user JWT as an HTTP-only cookie upon providing valid
    login credentials (email and password). It also returns the access and
    refresh token expiration dates in the response body. 

    This is where login requests should go from the frontend. 
    """

    def post(self, request, *args, **kwargs):
        try:
            user = authenticate(
                request, username=request.data['username'],
                password=request.data['password'])

            if user:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.avatar:
                    avatar = user_profile.avatar.url
                else:
                    avatar = f'https://api.dicebear.com/6.x/identicon/png?scale=70&seed={user_profile.robot}'
                login(
                    request, user, backend='authentication.email_authentication_backend.EmailBackend')
                response = prepare_user_response(user, avatar)
                return response
            else:
                return HttpResponse({'There was a problem logging you in'}, status=status.HTTP_403_FORBIDDEN)

        except:
            return HttpResponse({'There was a problem logging you in'}, status=status.HTTP_400_BAD_REQUEST)


class RefreshAccessToken(APIView):

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.verify()
                access_token = token.access_token
                response = JsonResponse(
                    {'success': 'New access token retrieved'})
                response.set_cookie('access_token', str(
                    access_token), httponly=True, samesite='None', secure=True, domain=os.environ['COOKIE_DOMAIN'])
                return response
            except Exception as e:
                print(e)
                return Response({'Invalid credentials'}, status=403)
        else:
            return Response({'Invalid credentials'}, status=403)


class LogoutUser(APIView):

    def post(self, request):
        try:
            response = JsonResponse({'message': 'Logged out successfully'})
            response.delete_cookie('access_token', samesite='None')
            response.delete_cookie('refresh_token', samesite='None')
            return response
        except Exception as e:
            print(e)
            return response


class CreateNewUser(APIView):

    def post(self, request):
        username = str(uuid.uuid4())
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if not all([username, email, password]):
            return Response({'error': 'Please provide an email and a password.'}, status=status.HTTP_400_BAD_REQUEST)

        elif email in User.objects.values_list('email', flat=True):
            print('YOU MADE IT IN HERE')
            return Response({'error': 'This email already exists in our system.'}, status=status.HTTP_400_BAD_REQUEST)

        elif not re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email):
            return Response({'error': 'You may have not entered a valid email'}, status=status.HTTP_400_BAD_REQUEST)

        elif len(email) > 100 or len(password) > 100:
            return Response({'error': 'Your email or password might be too long'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=username, email=email, password=password)
        except:
            return Response({'error': 'Failed to create user.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except Exception as e:
            print(e)
            return Response({'error': 'You likely forgot to specify your first or last name'}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = UserProfile.objects.get(user=user)
        dice_bear_avatar = ['Maggie', 'Mittens', 'Mia',
                                 'Pumpkin', 'Peanut', 'Socks', 'Jasmine', 'Snickers']
        user_profile.robot = random.choice(dice_bear_avatar)
        user_profile.save()

        avatar = f'https://api.dicebear.com/6.x/identicon/png?scale=70&seed={user_profile.robot}'
        response = prepare_user_response(user, avatar)

        return response


class GenerateAPIKey(viewsets.ModelViewSet):
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = APIKeySerializer
    queryset = APIKey.objects.all()
    lookup_field = 'key'

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data={'user': request.user.pk})

        if serializer.is_valid():
            print(serializer.errors)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response('unsuccessful', status=status.HTTP_400_BAD_REQUEST)
        
    def get_queryset(self):
        user = self.request.user
        api_keys = APIKey.objects.filter(user=user).order_by('read_only')
        return api_keys