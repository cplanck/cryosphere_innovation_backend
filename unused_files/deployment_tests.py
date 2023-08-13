import json
from unittest.mock import patch
from urllib.parse import urlencode

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from instruments.models import Deployment, Instrument
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class TestCreateAndGetInternalDeployment(APITestCase):

    """
    Test internal deployment endpoint. 
    Requests by user1 should show all of instrument1s and instrument2s deployments, 
    as they are the owner on instrument1.

    """

    def setUp(self):

        self.user1 = User.objects.create_user(
            email='testuser1@example.com',
            password='testpassword',
            username='testusername1',
            is_staff='True',
        )

        self.user2 = User.objects.create_user(
            email='testuser1@example.com',
            password='testpassword',
            username='testusername2',
        )

        self.user1_access_token = str(AccessToken.for_user(self.user1))
        self.user2_access_token = str(AccessToken.for_user(self.user2))

        instrument1 = Instrument.objects.create(
            name='Instrument with private deployment', serial_number='1', owner=self.user1)

        instrument1_deployment1 = Deployment.objects.create(
            name='Private Deployment 1', instrument=instrument1, private=True)

        instrument1_deployment2 = Deployment.objects.create(
            name='Private Deployment 1', instrument=instrument1)

        instrument2 = Instrument.objects.create(
            name='Instrument without private deployment', serial_number='2')

        instrument2_deployment1 = Deployment.objects.create(
            name='Private Deployment 1', instrument=instrument2)

    def test_user1_get_deployments(self):
        url = reverse('internal_deployments-list')

        # user1 should see three deployments (no instrument query param)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # user1 should see two deployments with an instrument1 id passed as a query param
        instrument1_id = Instrument.objects.filter(
            serial_number='1').values_list('id', flat=True)[0]
        params = {'instrument': instrument1_id}
        query_string = urlencode(params)
        url = reverse('internal_deployments-list') + '?' + query_string
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGetDeploymentWhenUserIsCollaborator(APITestCase):

    """
    Get deployments when user is listed as a collaborator on a deployment
    """

    def setUp(self):

        self.user1 = User.objects.create_user(
            email='testuser1@example.com',
            password='testpassword',
            username='testusername1',
            is_staff='True',
        )

        self.user2 = User.objects.create_user(
            email='testuser1@example.com',
            password='testpassword',
            username='testusername2',
        )

        self.user1_access_token = str(AccessToken.for_user(self.user1))
        self.user2_access_token = str(AccessToken.for_user(self.user2))

        instrument1 = Instrument.objects.create(
            name='Instrument with private deployment', serial_number='1', owner=self.user1)

        instrument1_deployment1 = Deployment.objects.create(
            name='Private Deployment 1', instrument=instrument1, private=True)
        instrument1_deployment1.collaborators.set([self.user2])

        instrument1_deployment2 = Deployment.objects.create(
            name='Private Deployment 2', instrument=instrument1, private=True)

        instrument2 = Instrument.objects.create(
            name='Instrument with public deployment', serial_number='2')

        instrument2_deployment1 = Deployment.objects.create(
            name='Public Deployment', instrument=instrument2)

    def test_user2_get_deployments(self):
        url = reverse('internal_deployments-list')

        # user2 should see 2 deployments (no instrument query param) because there are three
        # total. One public, two private, but one of the privates they are listed as collaborator on.

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user2_access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # user2 should see one deployments with an instrument1 id passed as a query param,
        # as they are only listed as a collaborator on one.
        instrument1_id = Instrument.objects.filter(
            serial_number='1').values_list('id', flat=True)[0]
        params = {'instrument': instrument1_id}
        query_string = urlencode(params)
        url = reverse('internal_deployments-list') + '?' + query_string
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user2_access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGetDeploymentsWhenUnauthenticated(APITestCase):

    """
    Test the response when an unauthenticated asks for deployments. The primary use case
    of this test is to emulate when a non-authenticated user navigates to a deployment page (SIMB3 page)
    for example.

    When a request is made to /internal/deployments/serial_number it should return the first deployment. 
    Other deployments can be specified by appending a ?deployment=X query parameter. 

    PS. this might need to change later on as we refine how to handle multiple deployments.
    """

    def setUp(self):
        instrument1 = Instrument.objects.create(
            name='Instrument with private deployment', serial_number='1', internal=True)

        Deployment.objects.create(
            name='Public Deployment 1', instrument=instrument1, private=False)

        Deployment.objects.create(
            name='Public Deployment 2', instrument=instrument1, private=False)

    def test_get_all_public_deployments(self):
        url = reverse('internal_deployments-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data['results'])
        self.assertEqual(len(response.data['results']), 2)

    def test_get_public_deployment_by_serial_number(self):
        url = reverse('internal_deployments-detail', args=['1'])
        print(url)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)


class TestCreateDeploymentAsStaff(APITestCase):

    """
    Create a deployment.

    """

    def setUp(self):

        self.user1 = User.objects.create_user(
            email='testuser1@example.com',
            password='testpassword',
            username='testusername1',
            is_staff='True',
        )

        self.user2 = User.objects.create_user(
            email='testuser1@example.com',
            password='testpassword',
            username='testusername2',
        )

        self.user1_access_token = str(AccessToken.for_user(self.user1))
        self.user2_access_token = str(AccessToken.for_user(self.user2))

        self.instrument1 = Instrument.objects.create(
            name='Instrument with private deployment', serial_number='1', owner=self.user1)

    def test_user1_create_deployment(self):
        """
        Only staff users can create deployment instances on this endpoint
        """
        url = reverse('internal_deployments-list')

        data = {
            'name': 'SIMB3 Deployment #1',
            'deployment_number': '0',
            'location': 'Beaufort Sea',
            'private': True,
            'collaborators': [self.user1.id],
            'instrument': self.instrument1.id,
        }

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.data)

    def test_user2_create_deployment(self):
        """
        Non-staff users cannot create deployment instances on this endpoint
        """
        url = reverse('internal_deployments-list')

        data = {
            'name': 'SIMB3 Deployment #1',
            'deployment_number': '0',
            'location': 'Beaufort Sea',
            'private': True,
            'collaborators': [self.user1.id]
        }

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user2_access_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
