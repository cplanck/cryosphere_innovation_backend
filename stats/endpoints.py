from authentication.http_cookie_authentication import CookieTokenAuthentication
from rest_framework import pagination, status, viewsets
from rest_framework.permissions import (AllowAny, BasePermission, IsAdminUser,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import DeploymentDownload
from .serializers import (DeploymentDownloadSerializer, DeploymentDownloadPOSTSerializer)

class DeploymentDownloadEndpoint(viewsets.ModelViewSet):

    """
    Added 10 August 2023
    """

    authentication_classes = [CookieTokenAuthentication]
    queryset = DeploymentDownload.objects.all().order_by('date_added')
    serializer_class = DeploymentDownloadSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DeploymentDownloadSerializer
        else:
            return DeploymentDownloadPOSTSerializer
        
    def get_queryset(self):
        deployment = self.request.GET.get('deployment')
        deployment_downloads = self.queryset.filter(deployment=deployment).order_by('user').distinct('user')
        return deployment_downloads