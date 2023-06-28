import json
import os
import re
import urllib.parse
import uuid
from datetime import datetime, timedelta
from random import seed

import jwt
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from dotenv import load_dotenv
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
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
from user_profiles.serializers import UserProfileSerializer

from authentication.http_cookie_authentication import CookieTokenAuthentication

load_dotenv()


def prepare_user_response(user, avatar):
    """
    If user is authenticated, prepare their response. 
    """
    user_profile = UserProfile.objects.get(user=user)

    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token

    # access_token_expiration = jwt.decode(
    #     str(access_token), options={"verify_signature": False})['exp']
    # refresh_token_expiration = jwt.decode(
    #     str(refresh_token), options={"verify_signature": False})['exp']

    response = JsonResponse(
        {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'avatar': avatar,
            'profile': UserProfileSerializer(user_profile).data
        })

    print(response)
    response.set_cookie('access_token', str(
        access_token), httponly=True, samesite='None', secure=True)
    response.set_cookie('refresh_token', str(
        refresh_token), httponly=True, samesite='None', secure=True)

    return response


class CreateNewUser(APIView):

    def post(self, request):
        username = str(uuid.uuid4())
        email = request.data.get('email')
        password = request.data.get('password')

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

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({'access': str(access_token), 'refresh': str(refresh)}, status=status.HTTP_201_CREATED)


class GoogleOneTap(APIView):

    def post(self, request):
        try:
            user_info_from_google = id_token.verify_oauth2_token(
                request.data, requests.Request(), os.environ['GOOGLE_CLIENT_ID'])

            user = User.objects.get(email=user_info_from_google['email'])

            if user:
                try:
                    avatar = user_info_from_google['picture']
                except:
                    avatar = 'https://api.dicebear.com/6.x/bottts/png?seed=Snickers'
                    # Also check if a users uploaded an avatar...
                response = prepare_user_response(user, avatar)

                return response
            else:
                # create account...
                pass

        except Exception as e:
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
                avatar = ''
                response = prepare_user_response(user, avatar)
                return response
            else:
                return HttpResponse({'There was a problem logging you in'}, status=status.HTTP_403_FORBIDDEN)

        except:
            return HttpResponse({'There was a problem logging you in'}, status=status.HTTP_400_BAD_REQUEST)


class RefreshAccessToken(APIView):

    def post(self, request):
        print('THIS RAN')
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.verify()
                access_token = token.access_token
                response = JsonResponse(
                    {'success': 'New access token retrieved'})
                response.set_cookie('access_token', str(
                    access_token), httponly=True, samesite='None', secure=True)
                return response
            except Exception as e:
                print(e)
                return Response({'Invalid credentials'}, status=403)
        else:
            return Response({'Invalid credentials'}, status=403)


class LogoutUser(APIView):

    def post(self, request):
        response = JsonResponse({'message': 'Logged out successfully'})
        response.delete_cookie('access_token')  # samesite='None'
        response.delete_cookie('refresh_token')
        return response
