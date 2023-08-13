from authentication.api_key_authentication import APIKeyAuthentication
from authentication.http_cookie_authentication import CookieTokenAuthentication
from authentication.models import APIKey
from data.dynamodb import *
from data.mongodb import *
from django.db.models import Q
from django.shortcuts import render
from rest_framework import pagination, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import (AllowAny, BasePermission, IsAdminUser,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from instruments.base_models import InstrumentSensorPackage

from .deployment_permissions_filter import deployment_permissions_filter
from .models import Deployment, Instrument
from .serializers import (DeploymentGETSerializer, DeploymentSerializer,
                          InstrumentPOSTSerializer,
                          InstrumentSensorPackageSerializer,
                          InstrumentSerializer)
from .permissions import CheckDeploymentReadWritePermissions



class InstrumentPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class InstrumentEndpoint(viewsets.ModelViewSet):
    """
    Endpoint for CRUD on Instrument model.
    
    Updated 12 August 2023
    """
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    serializer_class = InstrumentSerializer
    pagination_class = InstrumentPagination
    queryset = Instrument.objects.order_by('-last_modified')

    def create(self, request):

        if request.user.is_staff or request.user.userprofile.beta_tester:
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                errors = serializer.errors
                print(errors)
                return Response('There was a problem with your request', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeploymentPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class DeploymentEndpoint(viewsets.ModelViewSet):

    """
    Endpoint for CRUD on the deployment model. 
    
    Permissions are granted according to the model laid out in 
    permissions.py. 

    This view is used internally (by the frontend) and is not publically 
    exposed directly. It is the base class for the public and user endpoints.
    
    Updated 11 August, 2023
    """

    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [CheckDeploymentReadWritePermissions]
    pagination_class = DeploymentPagination
    lookup_field = 'slug'
    queryset = Deployment.objects.all().order_by('-last_modified')
    filterset_fields = ['status']
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DeploymentGETSerializer
        else:
            return DeploymentSerializer
        
    def partial_update(self, request, slug=None):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        return super().partial_update(request, slug=slug)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        return super().retrieve(request, *args, **kwargs)

    def create(self, request):
        # only allow staff and beta testing users to create
        if request.user.is_staff or request.user.userprofile.beta_tester:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response('There was a problem with your request', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, slug=None):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        return super().destroy(request, slug=slug)

    def get_queryset(self):
        return deployment_permissions_filter(self, self.queryset)
    


def strip_data_ends(data, strip_from_start, strip_from_end):
    print(strip_from_start)
    if strip_from_start:
        data = data[strip_from_start:]
    if strip_from_end:
        data = data[:-strip_from_end]
    return data


class DeploymentDataEndpoint(viewsets.ViewSet):

    """
    Main deployment data CRUD endpoint.
    Read/writes/deletes data from the MongoDB collection specified by the data_uuid PK (required) in the URL
    
    Updated 11 August 2023
    """
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [CheckDeploymentReadWritePermissions]
    http_method_names = ['get', 'patch', 'delete']

    def list(self, request):
        return Response('Detail not found. You likely forgot to include a /data_uuid in your URI.', status=status.HTTP_400_BAD_REQUEST)

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
            return Response({'There was a problem adding data to the database.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        object = Deployment.objects.get(data_uuid=pk)
        self.check_object_permissions(request, object)
        delete_count = delete_objects_from_mongo_db_collection_by_id(pk, request.data)
        return Response({'delete_count': delete_count}, status=status.HTTP_200_OK)



class InstrumentSensorPackageEndpoint(viewsets.ModelViewSet):
    """
    Endpoint for CRUD on the InstrumentSensorPackage model.

    Updated 12 August 2023
    """
     
    authentication_classes = [CookieTokenAuthentication]
    serializer_class = InstrumentSensorPackageSerializer
    queryset = InstrumentSensorPackage.objects.all().order_by('-last_modified')