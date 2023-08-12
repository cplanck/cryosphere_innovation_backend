import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from data.mongodb import delete_mongodb_collection

# from .endpoints import *
from instruments.models import Deployment, Instrument
from authentication.models import APIKey

class TestPublicDeploymentDataEndpoint(APITestCase):
    
    """
    Test public deployment data endpoint. Rules are:
    -API key required for all requests
    -If deployment is public, anyone can make a GET request
    -If deployment is private, only owner and collaborators can make GET request
    -Currently POST, PUT, PATCH, DELETE are dissallowed
    """

    def setUp(self):
        self.owner = User.objects.create_user(
            email='owner@example.com',
            password='owner',
            username='owner',
        )
        self.collaborator = User.objects.create_user(
            email='collaborator@example.com',
            password='collaborator',
            username='collaborator',
        )
        self.regular_user = User.objects.create_user(
            email='regular_user@example.com',
            password='regular_user',
            username='regular_user',
        )

        self.owner_api_key = APIKey(user=self.owner)
        self.collaborator_api_key = APIKey(user=self.collaborator)
        self.regular_user_api_key = APIKey(user=self.regular_user)

        self.owner_instrument = Instrument.objects.create(
            name='Test instrument #1', owner=self.owner)
        
        self.public_deployment = Deployment.objects.create(
            name='Test public deployment #1', private=False)
        
        self.client.credentials(
            HTTP_AUTHORIZATION='AUTHORIZATION' + self.user1_access_token)
        
        data=[{'time_stamp': 1.2345, 'air_temp': 23.322},
            {'time_stamp': 1.2346, 'air_temp': 23.322},
            {'time_stamp': 1.2347, 'air_temp': 23.322},]
        
        # fill collection with some fake data
        url = reverse('public_data_endpoint')
        response = self.client.post(url, data, format='json')

        
    def tearDown(self):
        # when test is done, delete collection 
        delete_mongodb_collection(self.public_deployment.data_uuid)

