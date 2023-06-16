import json
import stat
from unittest.mock import patch
from urllib.parse import urlencode

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from instruments.models import Deployment, Instrument
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class TestAddDataToDynamoTable(APITestCase):

    """
    Create an instrument and a deployment, add some data to the database,
    fetch the data and compare. Must be a staff user to POST

    Note: eventually, we might want to return the uniqueID
    """

    def setUp(self):

        self.user1 = User.objects.create_user(
            email='testuser1@example.com',
            password='testpassword',
            username='testusername1',
            is_staff='True',
        )

        self.user2 = User.objects.create_user(
            email='testuser2@example.com',
            password='testpassword',
            username='testusername2',
            is_staff='False',
        )

        instrument1 = Instrument.objects.create(
            name='Instrument 1', serial_number='1', owner=self.user1)

        Deployment.objects.create(
            name='Deployment 1', instrument=instrument1, private=False)

        self.user1_access_token = str(AccessToken.for_user(self.user1))
        self.user2_access_token = str(AccessToken.for_user(self.user2))

    def test_get_and_post_data_by_staff_user(self):

        # Add data to a DynamoDB table by UUID (only staff have access)
        url = reverse('internal_post_data')
        deployment_uuid = Deployment.objects.get(name='Deployment 1').data_uuid
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        data = {
            'deployment_uuid': deployment_uuid,
            'data': [
                {'time_stamp': 1.2345, 'air_temp': 23.322},
                {'time_stamp': 1.2346, 'air_temp': 23.322},
                {'time_stamp': 1.2347, 'air_temp': 23.322},
            ], 'primary_key': 'time_stamp'}
        response = self.client.post(url, data, format='json')

        # Get request data with deployment UUID as the PK
        url = reverse('internal_get_data', args=[deployment_uuid])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user2_access_token)
        response = self.client.get(url)
        self.assertEqual(response.data, data['data'])
        print(response.data)

        # Make sure non-staff users can't make POST requests
        url = reverse('internal_post_data')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user2_access_token)
        response = self.client.post(url, data, format='json')

        print(response)
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

        # Other tests we should write...
        #   - Proper error handling. What happens if you give an invalid UUID?
        #   - Authorization. We need to add privacy restrictions
