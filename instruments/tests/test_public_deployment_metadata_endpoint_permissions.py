
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from data.mongodb import delete_mongodb_collection

from instruments.models import Deployment, Instrument
from authentication.models import APIKey

# DEPLOYMENT METADATA ENDPOINT TESTS @/public/deployments/ 
# Written 12 August 2023

class TestPublicDeploymentMetadataPermissions(APITestCase):
    
    """    
    Test for verifying the permissions model for public (non-private) deployment metadata.
    Rules are:
    -API key required for all requests
    -Deployment is public, so anyone can make a GET request
    -All methods besides GET are disallowed

    RUN THESE TESTS WITH:
    python3 manage.py test instruments.tests.test_public_deployment_metadata_endpoint_permissions --keepdb
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
        self.public_user = User.objects.create_user(
            email='regular_user@example.com',
            password='regular_user',
            username='regular_user',
        )
        self.owner_api_key = APIKey.objects.create(user=self.owner)
        self.collaborator_api_key = APIKey.objects.create(user=self.collaborator)
        self.public_user_api_key = APIKey.objects.create(user=self.public_user)

        self.owner_instrument = Instrument.objects.create(
            name='Test instrument #1', owner=self.owner)
        
        self.public_deployment = Deployment.objects.create(
            name='Test public deployment #1', instrument=self.owner_instrument, private=False, slug='test-deployment-slug')
        self.public_deployment.collaborators.set([self.collaborator])

    def test_public_deployment_data_endpoint_permissions(self):
        """
        What we expect:
        Deployment is public, so 
        - all users can GET metadata
        - all other HTTP methods are currently forbidden (deployments should be edited via dashboard)
        """
        # make sure an API key is required. Should fail.
        id=self.public_deployment.slug
        url = reverse('public_deployment_endpoint-detail', args=[id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # public user GET request to public deployment. Should pass. 
        id=self.public_deployment.slug
        url = reverse('public_deployment_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.public_user_api_key.key}
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # all other methods besides GET are forbidden, even with a write-access API key
        # PATCH
        self.owner_api_key.read_only = False
        self.owner_api_key.save()
        id=self.public_deployment.slug
        url = reverse('public_deployment_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.owner_api_key.key}
        response = self.client.patch(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # POST
        self.owner_api_key.read_only = False
        self.owner_api_key.save()
        id=self.public_deployment.slug
        url = reverse('public_deployment_endpoint-list')
        headers = {'AUTHENTICATION': self.owner_api_key.key}
        response = self.client.post(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # DELETE
        self.owner_api_key.read_only = False
        self.owner_api_key.save()
        id=self.public_deployment.slug
        url = reverse('public_deployment_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.owner_api_key.key}
        response = self.client.delete(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        #PUT...

    def tearDown(self):
        # when test is done, delete MongoDB collection 
        name = self.public_deployment.data_uuid
        delete_mongodb_collection(str(name))


class TestPrivateDeploymentMetadataPermissions(APITestCase):
    
    """    
    Test for verifying the permissions model for metadata of private deployments.
    Rules are:
    -API key required for all requests
    -Deployment is private, so only owner and collaborators can make a GET request
    -All other methods besides GET are forbidden

    RUN THESE TESTS WITH:
    python3 manage.py test instruments.tests.test_public_deployment_metadata_endpoint_permissions --keepdb
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
        self.public_user = User.objects.create_user(
            email='regular_user@example.com',
            password='regular_user',
            username='regular_user',
        )
        self.owner_api_key = APIKey.objects.create(user=self.owner)
        self.collaborator_api_key = APIKey.objects.create(user=self.collaborator)
        self.public_user_api_key = APIKey.objects.create(user=self.public_user)

        self.owner_instrument = Instrument.objects.create(
            name='Test instrument #1', owner=self.owner)
        
        self.private_deployment = Deployment.objects.create(
            name='Test public deployment #1', instrument=self.owner_instrument, private=True, slug='test-deployment-slug')
        self.private_deployment.collaborators.set([self.collaborator])

    def test_public_deployment_data_endpoint_permissions(self):
        """
        What we expect:
        Deployment is private, so GET requests should from anyone other than owner or collaborator. 
        """
        # make sure an API key is required. Should fail.
        id=self.private_deployment.slug
        url = reverse('public_deployment_endpoint-detail', args=[id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # public user GET request to private deployment. Should fail. 
        id=self.private_deployment.slug
        url = reverse('public_deployment_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.public_user_api_key.key}
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # view responds to an empty queryset with a 404

        # owner user GET request to private deployment. Should pass. 
        id=self.private_deployment.slug
        url = reverse('public_deployment_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.owner_api_key.key}
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # collaborator user GET request to private deployment. Should pass. 
        id=self.private_deployment.slug
        url = reverse('public_deployment_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.collaborator_api_key.key}
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response to non-get requests were tested above.

    def tearDown(self):
        # when test is done, delete MongoDB collection 
        name = self.private_deployment.data_uuid
        delete_mongodb_collection(str(name))