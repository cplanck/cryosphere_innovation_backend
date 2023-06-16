import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from user_profiles.models import UserProfile


class UserPrfileTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            email='testuser1@example.com',
            password='testpassword',
            username='testusername1',
        )

        self.user1_access_token = str(AccessToken.for_user(self.user1))

    def test_user_profile_get_request(self):
        """
        Get a users users user profile
        """

        url = reverse('user_profile-list')

        # Test unauthenticated request -- password required
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.get(url, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            all(key in dict(response.data[0]) for key in ['id', 'full_name', 'avatar', 'social_login', 'has_social_avatar', 'has_made_deployment', 'has_made_instrument']))
