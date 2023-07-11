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


class InstrumentPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class InternalInstrumentEndpoint(viewsets.ModelViewSet):
    """
    Endpoint for CRUD on Instrument model for internally made
    instruments, e.g., SIMB3. The create() method is only available
    to staff users. list() returns a paginated response of istruments
    with internal = True.

    If an instrument has a deployment that with private=True, then it is
    automatically removed from public view unless the user viewing is either
    1) the owner of the instrument or 2) listed in the collaborators.


    The main purpose of this endpoint is for consumption by the CI frontend.
    It largely replaces the SIMB3 endpoint and instead returns all internal
    instruments.
    """
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    serializer_class = InstrumentSerializer
    pagination_class = InstrumentPagination
    queryset = Instrument.objects.filter(
        internal=True).order_by('-last_modified')

    def create(self, request):

        if request.user.is_staff:
            request.data._mutable = True
            request.data['internal'] = True
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


def check_key_permissions(self, pk, permissions):
    if '__all__' in permissions:
        return True
    elif pk in permissions:
        return True
    else:
        return False


class DeploymentPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class InternalDeploymentEndpoint(viewsets.ModelViewSet):

    """
    Endpoint for returning users deployments, either all or by ID. Handles
    all CRUD. For GET requests it returns an instrument object with each
    deployment. For POST/PUT/PATCH requests it accepts only an ID for instrument.

    This endpoint does a couple things
    -Return deployment(s) when given an instrument_id as a query param (main use cases for CI frontend)
    -Return the list of deployments that meet the following criteria
        - Are public (private=False)
        - Are of instruments they are listed as owners on
        - Are deployments that they are listed as collaborators on

    As of 2 June, 2023
    -Need to add authentication
    """

    authentication_classes = [CookieTokenAuthentication]
    pagination_class = DeploymentPagination
    lookup_field = 'slug'
    queryset = Deployment.objects.all().order_by('-last_modified')
    filterset_fields = ['status']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DeploymentGETSerializer
        else:
            return DeploymentSerializer

    def create(self, request):

        if request.user.is_staff:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response('There was a problem with your request', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        # Check if Authorization key was passed (for machine permissions).
        if 'Authorization' in self.request.headers:
            try:
                permissions = APIKey.objects.get(
                    key=self.request.headers['Authorization']).permissions[0]['deployments']

            except:
                return deployment_permissions_filter(self, self.queryset)
            if check_key_permissions(self, '', permissions):
                print('YOU MADE IT')
                return self.queryset

        return deployment_permissions_filter(self, self.queryset)


def strip_data_ends(data, strip_from_start, strip_from_end):
    print(strip_from_start)
    if strip_from_start:
        data = data[strip_from_start:]
    if strip_from_end:
        data = data[:-strip_from_end]
    return data


class InternalDataEndpoint(viewsets.ViewSet):

    """
    Main deployment data CRUD endpoint. Accepts get/patch requests with a PK (data_uuid)
    specified. 

    GET requests return the entire data
    Patch requests (for adding data to the MongoDB) require an API key with valid permissions.
    The permissions is a JSON where the data_uuid must be in the  deployments list, 
    ie., deployment : [data_uuid_1, data_uuid_2]

    Written 12 June 2023
    """
    authentication_classes = [CookieTokenAuthentication]

    def list(self, request):
        return Response('Method not allowed. You likely forgot to include a /data_uuid in your URI.', status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = deployment_permissions_filter(
            self,  Deployment.objects.all()).filter(data_uuid=pk)

        if queryset:
            strip_ends = queryset.values_list(
                'rows_from_start', 'rows_from_end')
            rows_from_start = strip_ends[0][0]
            rows_from_end = strip_ends[0][1]
            fields = request.query_params.getlist('field')
            data = get_data_from_mongodb(pk, fields)
            stripped_data = strip_data_ends(
                data, rows_from_start, rows_from_end)
            return Response(stripped_data, status=status.HTTP_200_OK)
        else:
            return Response('You don\'t have permission to perform this action.', status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, pk):
        try:
            key = self.request.headers['Authorization']
        except:
            return Response('Invalid API key. You might have a malformed Authorization header.', status=status.HTTP_400_BAD_REQUEST)
        try:
            permissions = APIKey.objects.get(
                key=key).permissions[0]['deployments']
        except:
            return Response('Bad API key', status=status.HTTP_400_BAD_REQUEST)

        if check_key_permissions(self, pk, permissions):
            response = post_data_to_mongodb_collection(pk, request.data)
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response('API key is either invalid or key doesnt have permissions.',
                            status=status.HTTP_400_BAD_REQUEST)


class InstrumentSensorPackageEndpoint(viewsets.ModelViewSet):
    authentication_classes = [CookieTokenAuthentication]
    serializer_class = InstrumentSensorPackageSerializer
    queryset = InstrumentSensorPackage.objects.all().order_by('-last_modified')

# ---------


class SIMB3MigrationEndpoint(viewsets.ModelViewSet):

    """
    Temporary endpoint for porting SIMB3s from the old system to the new system

    """
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    serializer_class = InstrumentSerializer
    pagination_class = InstrumentPagination

    def create(self, request):

        print(request.data)
        data = request.data
        data['internal'] = True
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response('There was a problem with your request', status=status.HTTP_400_BAD_REQUEST)


class SIMB3DeploymentMigrationEndpoint(viewsets.ViewSet):

    """
    Temporary endpoint for porting SIMB3s deployment data from the old system to the new system
    """

    def partial_update(self, request, *args, **kwargs):
        instrument_id = kwargs['pk']

        deployment_to_update = Deployment.objects.get(
            instrument=instrument_id)

        deployment_to_update = Deployment.objects.get(instrument=instrument_id)
        serializer = DeploymentSerializer(
            deployment_to_update, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'Deployment updated'}, status=status.HTTP_200_OK)
        else:
            return Response({'There was a problem with the request'}, status=status.HTTP_400_BAD_REQUEST)


class DeploymentData(viewsets.ViewSet):

    """
    Given a deployment ID, return raw data from DynamoDB.

    For SIMB3s, we need a way to work with the old IMEI based URL scheme.
    When a user navigates to /simb3/30043406... we need to fetch the the proper data.
    Could append a query parameter like ?deployment=1 or keep it implied
    """
    pass


class GetSIMB3InstrumentByIMEI(viewsets.ViewSet):

    """
    Given an IMEI, return the instrument details.
    """

    def list(self, request, *args, **kwargs):
        imei = kwargs['pk']
        print(imei)
        return Response({imei}, status=status.HTTP_200_OK)
