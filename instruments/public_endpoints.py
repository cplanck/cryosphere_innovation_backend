from authentication.api_key_authentication import APIKeyAuthentication
from authentication.models import APIKey
from rest_framework import pagination, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import (AllowAny, BasePermission, IsAdminUser,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from data.mongodb import *

from .deployment_permissions_filter import deployment_permissions_filter
from .models import Deployment, Instrument
from .serializers import (DeploymentGETSerializer, DeploymentSerializer,
                          InstrumentPOSTSerializer,
                          InstrumentSensorPackageSerializer,
                          InstrumentSerializer)
from .permissions import CheckDeploymentReadWritePermissions

def strip_data_ends(data, strip_from_start, strip_from_end):
    print(strip_from_start)
    if strip_from_start:
        data = data[strip_from_start:]
    if strip_from_end:
        data = data[:-strip_from_end]
    return data

class PublicDataEndpoint(viewsets.ViewSet):

    """
    Public endpoint for returning deployment data. This endpoint is exposed to the world and gives
    users authenticated with an API key access to data. 

    RULES:
    - A PK (data_uuid) must always be passed to designate a collection to choose from. 
    - For public deployments, RETREIVE access is granted to all
    - For private deployments, RETREIVE access is granted to owner and collaborators only

    TESTING: this endpoint is tested using public_data_endpoint_tests.py

    Written 12 August 2023
    """
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [CheckDeploymentReadWritePermissions]

    def list(self, request):
        return Response('Method not allowed. You likely forgot to include a /data_uuid in your URI.', status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        object = Deployment.objects.get(data_uuid=pk)
        self.check_object_permissions(request, object)
        fields = request.query_params.getlist('field')
        data = get_data_from_mongodb(pk, fields)
        stripped_data = strip_data_ends(
            data, object.rows_from_start, object.rows_from_end)
        return Response(stripped_data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk):
        object = Deployment.objects.get(data_uuid=pk)
        self.check_object_permissions(request, object)
        try:
            response = post_data_to_mongodb_collection(pk, request.data)
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'There was a problem adding data to the database.'})

