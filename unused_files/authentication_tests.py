import json

from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class AuthTests(APITestCase):

    """
    Test standard (non-social) login, logout, and user creation functionality
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testusername',
        )

    def test_successful_user_creation(self):
        """
        Successful user creation when given an email, and password
        """
        url = reverse('create new user')
        data = {
            'email': 'testuser2@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)
        print(response.data)

    def test_duplicated_user_creation(self):
        """
        Unsuccessful user creation when given an email that already exists
        """
        url = reverse('create new user')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        print(response.data)

    def test_user_creation_with_invalid_email(self):
        """
        Unsuccessful user creation when given an invalid email
        """
        url = reverse('create new user')
        data = {
            'email': 'testuserexample.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        print(response.data)

    def test_email_or_password_too_long(self):
        """
        Unsuccessful user creation when given an email or password thats too long
        """
        url = reverse('create new user')
        data = {
            'email': 'testudssadcasdcsadcascascsdacsdcsdcsadcasdcasdcsadcasdcasdcasdcascascasdcsacasdcasdcasdcasdcasdcasdcasdcasdcascsadcser@example.com',
            'password': 'testudssadcasdcsadcascascsdacsdcsdcsadcasdcasdcsadcasdcasdcasdcascascasdcsacasdcasdcasdcasdcasdcasdcasdcasdcascsadcser'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        print(response.data)

    def test_user_login(self):
        """
        Successful login with email and password and JWTs access/refresh returned
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_login_with_bad_password(self):
        """
        Unsuccessful login with bad password
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser@example.com',
            'password': 'testpasswordBAD',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('access' in response.data)
        self.assertFalse('refresh' in response.data)

    def test_login_with_bad_email(self):
        """
        Unsuccessful login with bad password
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuserBAD@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('access' in response.data)
        self.assertFalse('refresh' in response.data)

    def test_token_refresh(self):
        """
        Get refreshed access token with POST requestion
        """
        login_url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(login_url, data, format='json')
        refresh_token = response.data['refresh']

        refresh_url = reverse('token_refresh')
        data = {
            'refresh': refresh_token
        }
        response = self.client.post(refresh_url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        print(response.data)
        self.assertTrue('access' in response.data)

    def test_token_refresh_with_bad_refresh_token(self):
        """
        Get refreshed access token with POST requestion
        """
        login_url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(login_url, data, format='json')
        refresh_token = response.data['refresh']

        refresh_url = reverse('token_refresh')
        data = {
            'refresh': refresh_token + 'BAD'
        }
        response = self.client.post(refresh_url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)
