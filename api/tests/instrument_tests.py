import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from ..models import Instrument


class InstrumentTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            email='testuser1@example.com',
            password='testpassword',
            username='testusername1',
        )

        self.user2 = User.objects.create_user(
            email='testuser2@example.com',
            password='testpassword',
            username='testusername2',
        )

        self.instrument = Instrument.objects.create(
            user=self.user1,
            name='Test Instrument 1',
            description='This is a test instrument',
            avatar='test.png',
            serial_number='12345678910',
            starred=True,
            starred_date='2020-04-02T08:02:17-05:00',
        )
        self.instrument = Instrument.objects.create(
            user=self.user2,
            name='Test Instrument 2',
            description='This is a test instrument',
            avatar='test.png',
            serial_number='12345678910',
            starred=True,
            starred_date='2020-04-02T08:02:17-05:00',
        )
        self.instrument = Instrument.objects.create(
            user=self.user2,
            name='Test Instrument 3',
            description='This is a test instrument',
            avatar='test.png',
            serial_number='12345678910',
            starred=True,
            starred_date='2020-04-02T08:02:17-05:00',
        )

        self.user1_access_token = str(AccessToken.for_user(self.user1))
        self.user2_access_token = str(AccessToken.for_user(self.user2))

    def test_instrument_get_request(self):
        """
        Get all instruments for user1 and make sure they can only see their own instruments
        """
        url = reverse('instruments-list')

        # Test unauthenticated request -- password required
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test authenticated request -- password required and only user1 instruments retured
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['user'], self.user1.id)
        self.assertEqual(len(response.data['results']), 1)

        # Test authenticated request -- password required and only user2 instruments retured
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user2_access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['user'], self.user2.id)
        self.assertEqual(len(response.data['results']), 2)
        self.assertTrue(
            all(key in dict(response.data['results'][0]) for key in ['id', 'user', 'name', 'description', 'avatar', 'serial_number', 'starred', 'starred_date', 'date_added', 'last_modified', 'template', 'data_model', 'active_deployment']))

        # Test get by id -- fetch the instrument that was just made
        id = dict(response.data['results'][0])['id']
        url = reverse('instruments-detail', args=[id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], id)

    def test_instrument_post_request(self):
        """
        Create a new instrument for a user and return the instrument details
        """
        url = reverse('instruments-list')

        data = {
            'user': self.user1.id,
            'name': 'User created instrument 1',
            'serial_number': '123456789103211',
            'description': 'This is a user created instrument',
            'notes': 'These are notes',
            # 'starred': 'false',
            # 'starred_date': '2020-04-02T08:02:17-05:00',
            # 'template': 'false',
            # 'avatar': 'Null' # cant make a post request without a valid file
        }

        print(url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.data)
        self.assertEqual(response.data['user'], self.user1.id)
        self.assertTrue(
            all(key in dict(response.data) for key in ['id', 'user', 'name', 'description', 'avatar', 'serial_number', 'starred', 'starred_date', 'date_added', 'last_modified', 'template', 'data_model', 'active_deployment']))

    def test_instrument_patch_request(self):
        """
        Update the details of an existing instrument
        Note: the id is appended to the URL as /id, not as a query param
        """

        url = reverse('instruments-list')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.get(
            url, format='json', content_type='application/json')

        id = response.data['results'][0]['id']
        print(id)
        patch_url = reverse('instruments-detail', args=[id])
        data = {'description': 'This description has been modified by a patch update!'}
        response = self.client.patch(patch_url, data)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['description'] ==
                        'This description has been modified by a patch update!')

    def test_delete_instrument_by_id(self):
        """
        Fetch a users instrument, delete an instrument by ID
        """

        # fetch user instruments
        url = reverse('instruments-list')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user2_access_token)
        response = self.client.get(url, format='json')
        self.assertTrue(len(response.data['results']) == 2)

        # issue request to delete first instrument
        id = response.data['results'][0]['id']
        delete_url = reverse('instruments-detail', args=[id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # fetch instruments again and verify the length is == 1 and the deleted
        # object doesnt exists in the response
        url = reverse('instruments-list')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user2_access_token)
        response = self.client.get(url, format='json')
        self.assertTrue(len(response.data['results']) == 1)
        self.assertTrue(response.data['results'][0]['id'] != id)
