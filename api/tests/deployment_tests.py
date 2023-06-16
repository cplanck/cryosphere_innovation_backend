import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from ..models import Deployment, Instrument


class DeploymentTest(APITestCase):

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

        self.user3 = User.objects.create_user(
            email='testuser3@example.com',
            password='testpassword',
            username='testusername3',
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

        self.deployment1 = Deployment.objects.create(
            user=self.user1,
            name='First deployment 1',
            status='active',
            instrument=self.instrument,
            location='New York, New York',
            description='First new deployment test!',
            notes='No notes for now',
            deployment_start_date='2020-04-02T08:02:17-05:00',
            deployment_end_date='2020-04-10T08:02:17-05:00',
            private=False,
            starred=False,
            starred_date='2020-04-10T08:02:17-05:00',
            date_added='2020-04-10T08:02:17-05:00',
            last_modified='2020-04-10T08:02:17-05:00',
        )
        self.deployment1.collaborators.set([self.user2.id])

        self.user1_access_token = str(AccessToken.for_user(self.user1))
        self.user2_access_token = str(AccessToken.for_user(self.user2))
        self.user3_access_token = str(AccessToken.for_user(self.user3))

    def test_deployment_get_request(self):
        """
        Get all deployments for a user1
        """

        url = reverse('deployments-list')

        # Test unauthenticated request -- password required
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test get request for a user
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data['results'][0])[
                         'user'], self.user1.id)

        # Test get request with ID
        id = dict(response.data['results'][0])['id']
        url = reverse('deployments-detail', args=[id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], id)
        self.assertTrue(
            all(key in dict(response.data['instrument']) for key in ['id', 'name', 'avatar']))

    def test_deployment_get_request_by_id(self):
        """
        Get deployment bt ID
        """
        id = str(Deployment.objects.all().values_list('id', flat=True)[0])
        print('the id is ' + id)
        url = reverse('deployments-detail', args=[id])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['id']), id)
        self.assertTrue(
            all(key in dict(response.data['instrument']) for key in ['id', 'name', 'avatar']))

    def test_deployment_get_request_by_instrument_id(self):
        """
        Get list of deployments for an instrument by providing its ID
        """

        instrument_id = str(
            Instrument.objects.all().values_list('id', flat=True)[0])
        print(instrument_id)
        url = reverse('deployments-list') + '?instrument=' + instrument_id
        print(url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deployment_post_request(self):
        """
        Create a new deployment. Currently we use different serializers for post/get requests, 
        so we just need to specify the instrument primary key (id) here. GET requests will still
        have name, avatar, id.
        """

        url = reverse('deployments-list')

        data = {
            'user': self.user1.id,
            'name': 'First deployment 1',
            'status': 'active',
            'instrument': self.instrument.id,
            'status': 'active',
            'location': 'New York, New York',
            'description': 'Deployment created from post request!',
            'notes': 'No notes for now',
            'deployment_start_date': '2020-04-02T08:02:17-05:00',
            'deployment_end_date': '2020-04-10T08:02:17-05:00',
            'private': 'false',
            'starred': 'true',
            'starred_date': '2020-04-10T08:02:17-05:00',
        }

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(isinstance(response.data['instrument'], int))
        self.assertTrue('id' in response.data)

    def test_deployment_patch_request(self):
        """
        Testing modifying an existing deployment by specifying one or more modified fields
        """

        url = reverse('deployments-list')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.get(url, format='json')

        id = response.data['results'][0]['id']
        url = reverse('deployments-detail', args=[id])

        data = {
            'user': self.user1.id,
            'name': 'This is a modified deployment name',
            'status': 'inactive',
            'location': 'Brooklyn, New York',
        }

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['name'] ==
                        'This is a modified deployment name')

    def test_delete_deployment_by_id(self):
        """
        Test fetching a users deployment by ID and delete it
        """

        # fetch user deployments
        url = reverse('deployments-list')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.get(url, format='json')
        self.assertTrue(len(response.data['results']) == 1)

        # issue request to delete first deployment
        id = response.data['results'][0]['id']
        delete_url = reverse('deployments-detail', args=[id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # verify that its been deleted
        url = reverse('deployments-list')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user2_access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
