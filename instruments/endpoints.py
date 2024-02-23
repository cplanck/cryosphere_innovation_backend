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
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from instruments.base_models import InstrumentSensorPackage

from .deployment_permissions_filter import deployment_permissions_filter
from .models import Deployment, Instrument, DeploymentMedia
from .serializers import (DeploymentGETSerializer, DeploymentSerializer,
                          InstrumentPOSTSerializer,
                          InstrumentSensorPackageSerializer,
                          InstrumentSerializer, DeploymentMediaSerializer)
from .permissions import CheckDeploymentReadWritePermissions
from django.shortcuts import render
from PIL import Image
from openai import OpenAI
import re
from .helper_functions import *




class InstrumentPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class InstrumentEndpoint(viewsets.ModelViewSet):
    """
    Endpoint for CRUD on Instrument model.
    
    Updated 12 August 2023
    """
    authentication_classes = [CookieTokenAuthentication]
    serializer_class = InstrumentSerializer
    pagination_class = InstrumentPagination
    queryset = Instrument.objects.order_by('-last_modified')
    search_fields = ['name','serial_number', 'instrument_type', 'owner__first_name', 'owner__last_name', 'owner__email', 'deployment__name']


    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    def get_queryset(self):
        refined_queryset = search_and_filter_queryset(self.queryset, self.request, self.search_fields, 'status')
        return refined_queryset
    

class DeploymentPagination(pagination.PageNumberPagination):
    page_size = 100
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
    queryset = Deployment.objects.all().order_by('status').order_by('-last_modified').prefetch_related('instrument', 'realtimedata', 'collaborators')
    filterset_fields = ['status', 'web_page_enabled']
    http_method_names = ['get', 'post', 'patch', 'delete']
    search_fields = ['name', 'location', 'status', 'data_uuid', 'slug' , 'instrument__name', 'instrument__serial_number', 'instrument__instrument_type', 'instrument__owner__first_name', 'instrument__owner__last_name', 'instrument__owner__email']

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
        queryset = deployment_permissions_filter(self, self.queryset)
        refined_queryset = search_and_filter_queryset(queryset, self.request, self.search_fields, 'status')
        return refined_queryset
    

class DeploymentDataEndpoint(viewsets.ViewSet):

    """
    Main deployment data CRUD endpoint.
    Read/writes/deletes data from the MongoDB collection specified by the data_uuid PK (required) in the URL.
    APIKeyAuthentication added 12 August for Lambda function 
    
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
            cleaned_data = []
            for row in request.data:
                cleaned_headers, cleaned_row_num = clean_headers(row)
                cleaned_row = replace_key_names(row, cleaned_headers)
                cleaned_data.append(cleaned_row)
            response = post_data_to_mongodb_collection(pk, cleaned_data)
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'There was a problem adding data to the database.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        object = Deployment.objects.get(data_uuid=pk)
        self.check_object_permissions(request, object)
        delete_count = delete_objects_from_mongo_db_collection_by_id(pk, request.data)
        return Response({'delete_count': delete_count}, status=status.HTTP_200_OK)


class DeploymentDataValidationEndpoint(viewsets.ViewSet):
    """
    Endpoint for validating user added deployment data. 

    Writted 17 February, 2024
    """

    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        print(self.request.data)

        if self.request.data['headers']:
            cleaned_headers, counter = clean_headers(self.request.data['headers'])
            return Response({'cleaned_headers': cleaned_headers, 'cleaned_counter': counter})

        else:
            return Response('No headers found in request')

class DeploymentDataMetaDataEndpoint(viewsets.ViewSet):
    """
    Get Metadata stats for a deployment MongoDB collection

    Writted 17 February, 2024
    """

    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]
    

    def retrieve(self, request, pk=None):
        collection_metadata, indexes = get_collection_metadata(str(pk))
        print(collection_metadata['size'])
        return Response({'count': collection_metadata['count'],  
                         'size': collection_metadata['size'], 
                         'storage_size': collection_metadata['storageSize'], 
                         'indexes': indexes
                         })

class InstrumentSensorPackageEndpoint(viewsets.ModelViewSet):
    """
    Endpoint for CRUD on the InstrumentSensorPackage model.

    Updated 12 August 2023
    """
     
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = InstrumentSensorPackageSerializer
    filterset_fields = ['template', 'user']
    queryset = InstrumentSensorPackage.objects.all()

class PredictSensorFields(viewsets.ViewSet):
    """
    Endpoint for returning instrument sensor fields using the OpenAI API. 
    Accepts POST requests with the headers stripped from user uploaded 
    sample datasheet.

    Updaated 22 December 2023
    """
    authentication_classes = [CookieTokenAuthentication]
    http_method_names = ['post']

    def create(self, request):
        client = OpenAI()

    #     stream = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": "You will be provided with a list of headers and your goal is to return a list of objects, where each object is the form {fieldName: value, databaseName: value, unit: value, decimal: value}.  If the header you receive is capitalized or has spaces, you should use it as the fieldName. You should then decapitalize it and replace any spaces with underscores. There should be no special characters in the databaseName, but the fieldName should look nice and be capitalized. You should also estimate a value for the unit. Examples are 'C' for temperatures, 'mBar' for pressures, and 'deg' for latitudes or longitudes. fieldName acronyms should be capitalized. Any number should use the # for the unit. Temperatures should default to deg C. Times should default to seconds or Unix. The output must always be a list of dictionaries/objects. Never truncate the output or print anything else."},
    #         {"role": "user", "content": str(request.data)},
    #         ],
    #     stream=True,
    # )
    #     for chunk in stream:
    #         if chunk.choices[0].delta.content is not None:
    #             print(chunk.choices[0].delta.content, end="")
            
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
            {"role": "system", "content": "You will be provided a string and your goal is to return an object in the form {fieldName: value, databaseName: value, unit: value, precision: value}.  If the string is capitalized, has spaces, or looks human readable you should use it as the fieldName. You should then modify the value to be machine readable, meaning it doesn’t have any capital letters, special characters, and you should replace any spaces with underscores and use it as a databaseName. You should also estimate a value for the unit based on the fieldName. Examples are 'C' for temperatures, 'mBar' for pressures, and 'deg' for latitudes or longitudes. fieldName acronyms should be capitalized. Any number should use the # for the unit. Temperatures should default to deg C. Times should default to seconds or Unix. The output must always be a single object. Never truncate the output or print anything else. Precision is the number of decimals to keep for each field."},{"role": "system", "content": "You will be provided a string that represents a header and your goal is to return an object in the form {fieldName: value, databaseName: value, unit: value, precision: value}.  If the string is capitalized, has spaces, or looks human readable you should use it as the fieldName. You should then modify the value to be machine readable, meaning it doesn’t have any capital letters, special characters, and you should replace any spaces with underscores and use it as a databaseName. You should also estimate a value for the unit based on the fieldName. Examples are 'C' for temperatures, 'mBar' for pressures, and 'deg' for latitudes or longitudes. fieldName acronyms should be capitalized. Any number should use the # for the unit. Temperatures should default to deg C. Times should default to seconds or Unix. The output must always be a single object. Never truncate the output or print anything else OR ASK ANY CLARIFYING QUESTIONS. Precision is the number of decimals to keep for each field."},
            {"role": "user", "content": str(request.data)},
            ],
        )

        return JsonResponse({'prediction': completion.choices[0].message.content}, status=status.HTTP_200_OK)


class AddUniqueIDtoDeploymentMongoDB(viewsets.ViewSet):

    """
    Temporary endpoint for programmatically adding unique indexes
    on MongoDB collections that were created without them. 

    Written 10 Feb 2024
    """
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request):
        data_uuid = request.data['data_uuid']
        unique_index = request.data['unique_index']
        deployment = Deployment.objects.get(data_uuid=data_uuid)
        if deployment:
            try:
                r = add_unique_index_to_mongodb_collection(str(deployment.data_uuid), unique_index)
                if r['status']:
                    print(unique_index)
                    deployment.unique_index=unique_index
                    deployment.save()
                    return JsonResponse({'status': True, 'message': f'unique index {unique_index} added'}, status=200)
                else:
                    print(r['message'])
                    return JsonResponse({'status': False, 'message': f'Error: {r["message"]}'}, status=400)

            except Exception as e:
                print(e)
                return JsonResponse({'status': False, 'message': f'Error: {str(e)}'}, status=400)
        else:
            return JsonResponse({'status': f'no deployment found'}, status=400)


def resize_image(image, long_edge_size):
    # Calculate new dimensions while maintaining aspect ratio
    width, height = image.size
    aspect_ratio = width / height
    if width > height:
        new_width = long_edge_size
        new_height = int(long_edge_size / aspect_ratio)
    else:
        new_width = int(long_edge_size * aspect_ratio)
        new_height = long_edge_size
    
    # Resize the image
    resized_image = image.resize((new_width, new_height))
    return resized_image

def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        
        # Process the original image
        original_image = Image.open(image)
        
        # Define the long edge size for each resized image
        long_edge_sizes = [100, 300, 600]
        
        # Resize the image to three different sizes
        for long_edge_size in long_edge_sizes:
            resized_image = resize_image(original_image, long_edge_size)
            
            # Save the resized image
            save_image(resized_image, f'{long_edge_size}_{image.name}')
        
    return render(request, 'upload_image.html')

class DeploymentMediaEndpoint(viewsets.ModelViewSet):

    """
    CRUD on Deployment media, like images, datafiles, etc., that
    the user uploades

    Written 19 Feb, 2024
    """

    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = DeploymentMedia.objects.all().order_by('-date_added')
    serializer_class = DeploymentMediaSerializer

    def create(self, request):

        print(request.data['size'])
        if int(request.data['size']) > 20 * 1024 * 1024:
            return Response({'error': 'file size too large'}, status=400)

        media = DeploymentMedia(
            deployment_id=request.data['deployment_id'],
            location=request.FILES['file'], 
            name=request.data['name'],
            type=request.data['type'], 
            size=request.data['size'])
        media.save()
        return Response('')
    
    def retrieve(self, request, pk=None):
        serialized_data = DeploymentMediaSerializer(self.queryset.filter(deployment=pk), many=True)
        return Response(serialized_data.data)