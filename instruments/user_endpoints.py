

from .deployment_permissions_filter import deployment_permissions_filter
from .models import Deployment, Instrument
from .endpoints import DeploymentEndpoint, InstrumentEndpoint, InstrumentSensorPackageEndpoint
from django.db.models import Q
from .helper_functions import *

class UserInstrumentEndpoint(InstrumentEndpoint):
    """
    Endpoint for CRUD user created instruments. Subclasses the base IntrumentEndpoint.
    Added 4 August 2023
    """
    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(owner=self.request.user)

        refined_queryset = search_and_filter_queryset(queryset, self.request, self.search_fields, 'last_modified')

        return refined_queryset


class UserDeploymentEndpoint(DeploymentEndpoint):
    """
    Endpoint for CRUD on user deployments. Subclasses DeploymentEndpoint with an overridden queryset. 
    Update 12 August 2023
    """

    def get_queryset(self):

        if self.request.user.is_staff:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(instrument__owner=self.request.user) 

        refined_queryset = search_and_filter_queryset(queryset, self.request, self.search_fields, 'status')
               
        return refined_queryset

class UserInstrumentSensorPackageEndpoint(InstrumentSensorPackageEndpoint):
    """
    Endpoint for user CRUD on user sensor packages. Subclasses InstrumentSensorPackage.
    Updated 12 August 2023
    """
    # def get_queryset(self):
    #     queryset = self.queryset.filter(user=self.request.user)
    #     return queryset