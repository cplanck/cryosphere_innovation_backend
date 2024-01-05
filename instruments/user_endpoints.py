

from .deployment_permissions_filter import deployment_permissions_filter
from .models import Deployment, Instrument
from .endpoints import DeploymentEndpoint, InstrumentEndpoint, InstrumentSensorPackageEndpoint
from django.db.models import Q

class UserInstrumentEndpoint(InstrumentEndpoint):
    """
    Endpoint for CRUD user created instruments. Subclasses the base IntrumentEndpoint.
    Added 4 August 2023
    """
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        else:
            queryset = self.queryset.filter(owner=self.request.user).order_by('-last_modified')
            return queryset


class UserDeploymentEndpoint(DeploymentEndpoint):
    """
    Endpoint for CRUD on user deployments. Subclasses DeploymentEndpoint with an overridden queryset. 
    Update 12 August 2023
    """
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        else:
            queryset = Deployment.objects.filter(instrument__owner=self.request.user).order_by('-last_modified')
            # queryset = self.queryset.filter(Q(instrument__owner=self.request.user) | Q(collaborators__in=[self.request.user])).order_by('-last_modified')
            return deployment_permissions_filter(self, queryset)

class UserInstrumentSensorPackageEndpoint(InstrumentSensorPackageEndpoint):
    """
    Endpoint for user CRUD on user sensor packages. Subclasses InstrumentSensorPackage.
    Updated 12 August 2023
    """
    # def get_queryset(self):
    #     queryset = self.queryset.filter(user=self.request.user)
    #     return queryset