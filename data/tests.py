import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from .endpoints import *
from instruments.models import Deployment, Instrument
from authentication.models import APIKey

# table_name = '30043406123455678'


# class DynamoDBTableTest(APITestCase):

#     """
#     Test creating a DynamoDB table called table_name, posting data to the table, 
#     fetching the data, and then finally deleting the table.
#     """

#     def test_add_table_data_and_delete(self):
#         # Create DynamoDB table
#         url = reverse('dynamodb_table_endpoint')
#         response = self.client.post(
#             url, {'table_name': table_name}, format='json')
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # Create new record under new DynamoDB table
#         url = reverse('dynamodb_post_data_endpoint')
#         data = {'table_name': table_name, 'data': {'uniqueID': '26', 'imei': '300434061234567', 'time_stamp': 12321121,
#                 'snow_distance': 12321.123, 'air_temp': 12.1231, 'bottom_distance': 1234.1231}}
#         response = self.client.post(url, data, format='json')
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # Fetch newly added record from DynamoDB table
#         url = reverse('dynamodb_get_data_endpoint', args=[table_name])
#         response = self.client.get(url, format='json')
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Delete table and all contents
#         url = reverse('dynamodb_table_endpoint')
#         response = self.client.delete(
#             url, {'table_name': table_name}, format='json')
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


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
        
        response = self.client.post(url, data, format='json')
