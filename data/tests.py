import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from .endpoints import *

table_name = '30043406123455678'


class DynamoDBTableTest(APITestCase):

    """
    Test creating a DynamoDB table called table_name, posting data to the table, 
    fetching the data, and then finally deleting the table.
    """

    def test_add_table_data_and_delete(self):
        # Create DynamoDB table
        url = reverse('dynamodb_table_endpoint')
        response = self.client.post(
            url, {'table_name': table_name}, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create new record under new DynamoDB table
        url = reverse('dynamodb_post_data_endpoint')
        data = {'table_name': table_name, 'data': {'uniqueID': '26', 'imei': '300434061234567', 'time_stamp': 12321121,
                'snow_distance': 12321.123, 'air_temp': 12.1231, 'bottom_distance': 1234.1231}}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Fetch newly added record from DynamoDB table
        url = reverse('dynamodb_get_data_endpoint', args=[table_name])
        response = self.client.get(url, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete table and all contents
        url = reverse('dynamodb_table_endpoint')
        response = self.client.delete(
            url, {'table_name': table_name}, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
