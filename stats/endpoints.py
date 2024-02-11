from authentication.http_cookie_authentication import CookieTokenAuthentication
from rest_framework import pagination, status, viewsets
from rest_framework.permissions import (AllowAny, BasePermission, IsAdminUser,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import DeploymentDownload
from .serializers import (DeploymentDownloadSerializer, DeploymentDownloadPOSTSerializer)
from instruments.models import Deployment

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
    

# class DeploymentDownloadStatsSummaryEndpoint(viewsets.ModelViewSet):

#     """
#     This endpoint is used in the Admin console to return summary statistics for deployment data downloads. 
    
#     Added 11 Feb 2024
#     """

#     authentication_classes = [CookieTokenAuthentication]
#     serializer_class = DeploymentDownloadStatsSummaryEndpoint
#     permission_classes = [IsAdminUser]
#     queryset = Deployment.objects.all()

