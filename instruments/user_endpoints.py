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


class UserInstrumentSensorPackageEndpoint(viewsets.ModelViewSet):
    authentication_classes = [CookieTokenAuthentication]
    serializer_class = InstrumentSensorPackageSerializer
    queryset = InstrumentSensorPackage.objects.all().order_by('-last_modified')

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

class InstrumentPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserInstrumentEndpoint(viewsets.ModelViewSet):
    """
    Endpoint for user created instruments
    Added 4 August 2023
    """
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    serializer_class = InstrumentSerializer
    pagination_class = InstrumentPagination
    queryset = Instrument.objects.order_by('-last_modified')

    def create(self, request):
        if request.user.userprofile.beta_tester:
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
    
    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset

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


class UserDeploymentEndpoint(viewsets.ModelViewSet):

    """
    Endpoint for CRUD on user created deployments
    Added 5 August 2023
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

        if request.user.userprofile.beta_tester:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response('There was a problem with your request', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        queryset = self.queryset.filter(instrument__owner=self.request.user)
        return queryset


def strip_data_ends(data, strip_from_start, strip_from_end):
    print(strip_from_start)
    if strip_from_start:
        data = data[strip_from_start:]
    if strip_from_end:
        data = data[:-strip_from_end]
    return data


class UserDataEndpoint(viewsets.ViewSet):

    """
    Endpoint for CRUD on user deployment data from the frontend. 

    Added 5 August 2023
    """
    authentication_classes = [CookieTokenAuthentication]

    def partial_update(self, request, pk):
        post_data_to_mongodb_collection(pk, request.data)
        return Response('Test endpoint', status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        delete_count = delete_objects_from_mongo_db_collection_by_id(pk, request.data)
        print('DELETE COUNT')
        print(request.data)
        print(delete_count)
        return Response({'is this': 'a json'}, status=status.HTTP_204_NO_CONTENT)

    # def list(self, request):
    #     return Response('Method not allowed. You likely forgot to include a /data_uuid in your URI.', status=status.HTTP_400_BAD_REQUEST)

    # def retrieve(self, request, pk=None):
    #     queryset = deployment_permissions_filter(
    #         self,  Deployment.objects.all()).filter(data_uuid=pk)

    #     if queryset:
    #         strip_ends = queryset.values_list(
    #             'rows_from_start', 'rows_from_end')
    #         rows_from_start = strip_ends[0][0]
    #         rows_from_end = strip_ends[0][1]
    #         fields = request.query_params.getlist('field')
    #         data = get_data_from_mongodb(pk, fields)
    #         stripped_data = strip_data_ends(
    #             data, rows_from_start, rows_from_end)
    #         return Response(stripped_data, status=status.HTTP_200_OK)
    #     else:
    #         return Response('You don\'t have permission to perform this action.', status=status.HTTP_401_UNAUTHORIZED)

    # def partial_update(self, request, pk):
    #     try:
    #         key = self.request.headers['Authorization']
    #     except:
    #         return Response('Invalid API key. You might have a malformed Authorization header.', status=status.HTTP_400_BAD_REQUEST)
    #     try:
    #         permissions = APIKey.objects.get(
    #             key=key).permissions[0]['deployments']
    #     except:
    #         return Response('Bad API key', status=status.HTTP_400_BAD_REQUEST)

    #     if check_key_permissions(self, pk, permissions):
    #         response = post_data_to_mongodb_collection(pk, request.data)
    #         return Response(response, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response('API key is either invalid or key doesnt have permissions.',
    #                         status=status.HTTP_400_BAD_REQUEST)


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
