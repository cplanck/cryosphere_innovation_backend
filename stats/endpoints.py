from authentication.http_cookie_authentication import CookieTokenAuthentication
from rest_framework import pagination, status, viewsets
from rest_framework.permissions import (AllowAny, BasePermission, IsAdminUser,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import DeploymentDownload
from .serializers import (DeploymentDownloadSerializer, DeploymentDownloadPOSTSerializer)
from instruments.models import Deployment, Instrument
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from user_profiles.serializers import UserSerializer
from real_time_data.models import SBDData, RealTimeData
from django.utils import timezone
from django.db.models import Q
import pytz
from general.models import WebsiteStatus
from general.serializers import WebsiteStatusSerializer


class DeploymentDownloadEndpoint(viewsets.ModelViewSet):

    """
    Given a deployment, this endpoint fetchs users that have downloaded data. User info, including
    name, avatar, and date downloaded are serialized and returned. 
    Added 10 August 2023
    """

    authentication_classes = [CookieTokenAuthentication]
    queryset = DeploymentDownload.objects.select_related('user', 'user__userprofile', 'deployment')

    serializer_class = DeploymentDownloadSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DeploymentDownloadSerializer
        else:
            return DeploymentDownloadPOSTSerializer
        
    def get_queryset(self):
        deployment = self.request.GET.get('deployment')
        if deployment:
            deployment_downloads = self.queryset.filter(deployment=deployment).order_by('user').distinct('user')
        else:
            deployment_downloads = self.queryset
        return deployment_downloads
    
class AdminStatsEndpoint(viewsets.ViewSet):

    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAdminUser]


    def list(self, request):

        utc_now = datetime.utcnow()
        ny_tz = pytz.timezone('America/New_York')
        ny_time = utc_now.astimezone(ny_tz)

        instruments = Instrument.objects.count()
        deployments = Deployment.objects.count()
        users = User.objects.count()

        website_status = WebsiteStatus.objects.all().first()
        website_status_serialized = WebsiteStatusSerializer(website_status)
       
        new_users = User.objects.filter(date_joined__gte=(ny_time - timedelta(days=7)))
        new_users_serialized = UserSerializer(new_users, many=True)

        sbd_files_downloaded_today = SBDData.objects.filter(date_added__gte=(ny_time - timedelta(days=1))).count()

        real_time_data_errors = RealTimeData.objects.exclude(Q(error__isnull=True) | Q(error='')).count()

        return Response({'instruments': instruments, 'deployments': deployments, 'users': users, 'new_users': new_users_serialized.data,'website_status':website_status_serialized.data ,'sbd_files_downloaded_today': sbd_files_downloaded_today, 'real_time_data_errors': real_time_data_errors})
