import json
from decimal import Decimal
from urllib import response

import boto3
from authentication.http_cookie_authentication import CookieTokenAuthentication
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from django.db.models import Q
from django.shortcuts import render
from rest_framework import pagination, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..data.dynamodb import *


class DataEndpointWrite(viewsets.ViewSet):

    def list(self, request):

        dynamodb_client = boto3.client('dynamodb')
        item = {
            'uniqueID': {'S': '1'},
            'name': {'S': 'John Doe'},
            'age': {'N': '30'},
            'email': {'S': 'johndoe@example.com'}
        }

        # Make the put_item request
        response = dynamodb_client.put_item(
            TableName='cryosphere-innovation-dynamodb',
            Item=item
        )

        return Response({'response': response})


class DataEndpointRead(viewsets.ViewSet):

    def list(self, request):

        dynamodb_client = boto3.client('dynamodb')

        # Make the put_item request
        response = dynamodb_client.get_item(
            TableName='cryosphere-innovation-dynamodb',
            Key={'uniqueID': {'S': '1'}}
        )

        deserializer = TypeDeserializer()
        deserialized_item = {key: deserializer.deserialize(
            value) for key, value in response['Item'].items()}

        return Response(deserialized_item)


class DynamoDBDataEndpoint(APIView):

    """
    CRUD on data in a DynamoDB table given a table name.
    """

    def get(self, request, table_name):
        response = get_data_from_dynamodb(table_name)
        if response:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response('There was a problem with your request', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        table_name = request.data['table_name']
        data = request.data['data']

        table_exists = check_if_dynamodb_table_exists(table_name)

        if table_exists:
            response = post_data_to_dynamodb_table(table_name, data)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return Response({'Data entry successfully added to ' + table_name}, status=status.HTTP_201_CREATED)
            else:
                return Response({'There was a problem with your request. Data entry may not have been added'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'There was a problem with your request. It is possible that table ' + table_name + ' does not exist or is still being created'}, status=status.HTTP_400_BAD_REQUEST)


class DynamoDBTableEndpoint(APIView):

    """
    Endpoint for creating and deleting DynamoDB tables. 
    """

    def post(self, request):
        """
        Creates a DynamoDB table of name table_name as specified in the POST request payload. 
        The table will be created with a string primary key called uniqueID,
        """

        table_name = request.data['table_name']
        table_exists = check_if_dynamodb_table_exists(table_name)
        if not table_exists:
            response = create_dynamodb_table(table_name)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return Response({'Table ' + table_name + ' successfully created'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'There was a problem with your request. The table ' + table_name + ' may not have been created'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'There was a problem with your request. It is possible that ' + table_name + ' already exists'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Deletes a table of name table_name as specified in the DELETE request payload. 
        """

        table_name = request.data['table_name']
        table_exists = check_if_dynamodb_table_exists(table_name)
        if table_exists:
            response = delete_dynamodb_table(table_name)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return Response({'Table ' + table_name + ' successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'There was a problem with your request. The table ' + table_name + ' may not have been deleted'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'There was a problem with your request'}, status=status.HTTP_400_BAD_REQUEST)
