from authentication.http_cookie_authentication import CookieTokenAuthentication
from django.db.models import Q
from django.shortcuts import render
from rest_framework import pagination, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Deployment, Instrument
from .serializers import (DeploymentGETSerializer, DeploymentSerializer,
                          InstrumentSerializer)


class InstrumentPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100


class InstrumentEndpoint(viewsets.ModelViewSet):
    """
    Endpoint for returning users instruments, either all or by ID. Handles
    all
    """
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = InstrumentSerializer
    pagination_class = InstrumentPagination

    try:
        def get_queryset(self):
            print(self.request.user)
            return Instrument.objects.filter(user=self.request.user).order_by('-last_modified')
    except Exception as e:
        print(e)


class DeploymentPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100


class DeploymentEndpoint(viewsets.ModelViewSet):

    """
    Endpoint for returning users deployments, either all or by ID. Handles
    all CRUD. For GET requests it returns an instrument object with each 
    deployment. For POST/PUT/PATCH requests it accepts only an ID for instrument.
    """
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DeploymentPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DeploymentGETSerializer
        else:
            return DeploymentSerializer

    def get_queryset(self):
        instrument_id = self.request.query_params.get('instrument')
        qs = Deployment.objects.filter(
            user=self.request.user).order_by('-last_modified')
        qs = qs if not instrument_id else qs.filter(
            instrument__id=instrument_id)
        return qs
