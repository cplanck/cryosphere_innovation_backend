from authentication.http_cookie_authentication import CookieTokenAuthentication
from authentication.models import APIKey
from rest_framework import pagination, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import (AllowAny, BasePermission, IsAdminUser,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from instruments.base_models import InstrumentSensorPackage

from .models import RealTimeData
from .serializers import (RealTimeDataSerializer,)


class RealTimeDataEndpoint(viewsets.ModelViewSet):

    """
    Endpoint for CRUD on the real-time data model. This model
    is used my the AWS lambda function to control what and how
    deployments get decoded, posted to the DB, etc. 
    """

    authentication_classes = [CookieTokenAuthentication]
    queryset = RealTimeData.objects.all().order_by('-last_modified')
    serializer_class = RealTimeDataSerializer
    filterset_fields = ['active']

