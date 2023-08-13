
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from data.mongodb import delete_mongodb_collection

from instruments.models import Deployment, Instrument
from authentication.models import APIKey

# DEPLOYMENT DATA ENDPOINT TESTS @/public/deployments/data
# Written 12 August 2023

class TestPublicDeploymentDataPermissions(APITestCase):
    
    """    
    Test for verifying the permissions model for public (non-private) deployments.  
    Rules are:
    -API key required for all requests
    -Deployment is public, so anyone can make a GET request
    -Only owner and collaborators can make PATCH/DELETE requests
    -POST and PUT methods are disallowed

    RUN THESE TESTS WITH:
    python3 manage.py test instruments.tests.test_public_deployment_data_endpoint_permissions --keepdb
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
            name='Test public deployment #1', instrument=self.owner_instrument, private=False)
        self.public_deployment.collaborators.set([self.collaborator])

    def test_public_deployment_data_endpoint_permissions(self):
        """
        What we expect:
        Deployment is public, so 
        - public users can GET data
        - owner can PATCH/DELETE data
        - collaborators can PATCH/DELETE data
        - all other HTTP methods are disallowed
        Note: owner/collaborators still must have a non-read-only API key
        """
        # make sure an API key is required. Should fail.
        id=self.public_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # public user GET request to public deployment. Should pass. 
        id=self.public_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.public_user_api_key.key}
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # owner user GET request to public deployment. Should pass.
        id=self.public_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.owner_api_key.key}
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # collaborator user GET request to public deployment. Should pass
        id=self.public_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.collaborator_api_key.key}
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # owner PATCH request. Should fail because API keys are read-only by default
        id=self.public_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.owner_api_key.key}
        response = self.client.patch(url, format='json', **headers, data={'hello':'world'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # collaborator PATCH request. Should fail because API keys are read-only by default
        id=self.public_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.collaborator_api_key.key}
        response = self.client.patch(url, format='json', **headers, data={'hello':'world'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # now flip owner key to read_only=False, and try again. 
        self.owner_api_key.read_only = False
        self.owner_api_key.save()
        id=self.public_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.owner_api_key.key}
        response = self.client.patch(url, format='json', **headers, data=[{'hello':'world', 'time_stamp': 1}])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # do the same with collaborator key (read_only=False): 
        self.collaborator_api_key.read_only = False
        self.collaborator_api_key.save()
        id=self.public_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.collaborator_api_key.key}
        response = self.client.patch(url, format='json', **headers, data=[{'hello':'world', 'time_stamp': 2}])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # now flip the public key. Test should fail as non-owners/collaborators never have write access
        self.public_user_api_key.read_only = False
        self.public_user_api_key.save()
        id=self.public_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.public_user_api_key.key}
        response = self.client.patch(url, format='json', **headers, data=[{'hello':'world', 'time_stamp': 3}])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # also make sure public cannot delete
        id=self.public_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.public_user_api_key.key}
        response = self.client.delete(url, format='json', **headers, data=[{'hello':'world', 'time_stamp': 3}])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # finally make sure that POST and PUT methods are forbidden
        # PUT
        id=self.public_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.owner_api_key.key}
        response = self.client.put(url, format='json', **headers, data=[{'hello':'world', 'time_stamp': 1}])
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # POST
        id=self.public_deployment.data_uuid
        url = reverse('public_data_endpoint-list')
        headers = {'AUTHENTICATION': self.owner_api_key.key}
        response = self.client.post(url, format='json', **headers, data=[{'hello':'world', 'time_stamp': 1}])
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def tearDown(self):
        # when test is done, delete MongoDB collection 
        name = self.public_deployment.data_uuid
        delete_mongodb_collection(str(name))

class TestPrivateDeploymentDataPermissions(APITestCase):
         
    """
    Test for verifying the permissions model for public (non-private) deployments.  
    Rules are:
    -API key required for all requests
    -Deployment is public, so anyone can make a GET request
    -Only owner and collaborators can make PATCH/DELETE requests
    -POST and PUT methods are disallowed
    
    Written 12 August 2023
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
            name='Test public deployment #1', instrument=self.owner_instrument, private=True)
        self.private_deployment.collaborators.set([self.collaborator])

    def test_private_deployment_data_endpoint_permissions(self):
        """
        What we expect:
        Deployment is private, so 
        - public users CANNOT make GET requests
        - owner can GET/PATCH/DELETE data
        - collaborators can GET/PATCH/DELETE data
        - all other HTTP methods are disallowed
        Note: owner/collaborators still must have a non-read-only API key for write access

        """
        # make sure an API key is required. Should fail.
        id=self.private_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # public user GET request to private deployment. Should FAIL. 
        id=self.private_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.public_user_api_key.key}
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # owner user GET request to private deployment. Should pass.
        id=self.private_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.owner_api_key.key}
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # collaborator user GET request to public deployment. Should pass
        id=self.private_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.collaborator_api_key.key}
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # make sure owner can PATCH with a write-access API key.
        self.owner_api_key.read_only = False
        self.owner_api_key.save()
        id=self.private_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.owner_api_key.key}
        response = self.client.patch(url, format='json', **headers, data=[{'hello':'world', 'time_stamp': 1}])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # do the same with collaborator key (read_only=False): 
        self.collaborator_api_key.read_only = False
        self.collaborator_api_key.save()
        id=self.private_deployment.data_uuid
        url = reverse('public_data_endpoint-detail', args=[id])
        headers = {'AUTHENTICATION': self.collaborator_api_key.key}
        response = self.client.patch(url, format='json', **headers, data=[{'hello':'world', 'time_stamp': 2}])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def tearDown(self):
        # when test is done, delete MongoDB collection 
        name = self.private_deployment.data_uuid
        delete_mongodb_collection(str(name))