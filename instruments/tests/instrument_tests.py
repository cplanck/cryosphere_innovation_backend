import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from instruments.models import Deployment, Instrument
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class TestCreateAndGetInternalInstrument(APITestCase):

    """
    CRUD on the Instrument model.The internal instrument endpoint only accepts 
    POST requests from staff members.

    In this test, we create an instrument with instrument_type = SIMB3 from an account
    marked is_staff which sets internal=True. Instruments with this classification 
    are the Cryosphere Innovation SIMB3s. Note: on creation, SIMB3 instantiation automatically
    create a deployment index. 

    Get request without an identifier should return a list of all internal
    instruments. With an identifier it should return a single instance.
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
            is_staff='False',
        )

        self.user1_access_token = str(AccessToken.for_user(self.user1))
        self.user2_access_token = str(AccessToken.for_user(self.user2))

    def test_crud_internal_instrument(self):

        url = reverse('internal_instruments-list')
        data = {
            'name': 'Cryosphere Innovation SIMB3 #1',
            'serial_number': '300434061234567',
            'owner': '',
            'instrument_type': 'SIMB3'
        }
        # Staff users can POST to internal instruments
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that Deployment model created (signal worked)
        deployment = Deployment.objects.get()
        self.assertEqual(
            deployment.name, 'Cryosphere Innovation SIMB3 #1 Deployment #1')

        # Make sure non-staff users cant POST to this endpoint
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user2_access_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Fetch all instruments that have internal = True
        url = reverse('internal_instruments-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Fetch instrument by ID when passed after slash
        id = Instrument.objects.all().values_list('id', flat=True)[0]
        url = reverse('internal_instruments-detail', args=[id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete instrument by ID
        deployment_count = Deployment.objects.filter(instrument=id).count()
        id = Instrument.objects.all().values_list('id', flat=True)[0]
        url = reverse('internal_instruments-detail', args=[id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        deployment_count = Deployment.objects.filter(instrument=id).count()
        self.assertEqual(deployment_count, 0)


class TestGetPrivateInternalInstrumentAsOwner(APITestCase):

    """
    Test instrument privacy controls. If an instrument has a deployment that is
    private, then it's only visible to the user listed as 'owner' or to any collaborators
    attached to the deployment. 

    In this test case we are testing that an 'owner' can see private instruments.
    """

    def setUp(self):
        self.user1 = User.objects.create_user(
            email='testuser1@example.com',
            password='testpassword',
            username='testusername1',
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

        Deployment.objects.create(
            name='Private Deployment 1', instrument=instrument1, private=True)

        instrument2 = Instrument.objects.create(
            name='Instrument without private deployment', serial_number='2')

    def test_when_user_is_owner(self):
        url = reverse('internal_instruments-list')

        # user1 should see instrument1 and instrument2, as they are owner on 1
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # user2 should only see instrument2, as it doesn't have any private deployments
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user2_access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGetPrivateInternalInstrumentWithCollaborators(APITestCase):

    """
    Test instrument privacy controls. If an instrument has a deployment that is
    private, then it's only visible to the user listed as 'owner' or to any collaborators
    attached to the deployment. 

    In this test case we are testing that an user added as a collaborator can see private instruments.
    """

    def setUp(self):
        self.user1 = User.objects.create_user(
            email='testuser1@example.com',
            password='testpassword',
            username='testusername1',
        )

        self.user2 = User.objects.create_user(
            email='testuser1@example.com',
            password='testpassword',
            username='testusername2',
        )

        self.user1_access_token = str(AccessToken.for_user(self.user1))
        self.user2_access_token = str(AccessToken.for_user(self.user2))

        instrument1 = Instrument.objects.create(
            name='Instrument with private deployment', serial_number='1')

        instrument2 = Instrument.objects.create(
            name='Instrument without private deployment', serial_number='2')

        deployment1 = Deployment.objects.create(
            name='Private Deployment 1', instrument=instrument1, private=True)
        deployment1.collaborators.set([self.user2])

    def test_when_user_is_collaborator(self):
        url = reverse('internal_instruments-list')

        # user1 should see only instrument2, as they are neither an owner nor a collaborator on instrument1
        # which has a private deployment
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user1_access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # user2 should see instrument1 and 2, as they are listed as a collaborator on instrument1's deployment
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.user2_access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
