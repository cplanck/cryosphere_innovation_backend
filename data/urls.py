from django.urls import include, path
from rest_framework import routers

from data.endpoints import *

urlpatterns = [
    path('create_table', DynamoDBTableEndpoint.as_view(),
         name='dynamodb_table_endpoint'),

    path('<str:table_name>', DynamoDBDataEndpoint.as_view(),
         name='dynamodb_get_data_endpoint'),

    path('', DynamoDBDataEndpoint.as_view(),
         name='dynamodb_post_data_endpoint'),
]
