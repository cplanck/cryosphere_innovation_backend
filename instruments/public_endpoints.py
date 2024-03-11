from authentication.api_key_authentication import APIKeyAuthentication
from .endpoints import DeploymentDataEndpoint, DeploymentEndpoint
from .serializers import PublicDeploymentGETSerializer, DeploymentGETSerializer, DeploymentSerializer

class PublicDataEndpoint(DeploymentDataEndpoint):

    """
    Publically exposed enpoint for CRUD on deployment data. Same
    thing as DeploymentDataEndpoint, but uses an API key for authentication.
    """
    authentication_classes = [APIKeyAuthentication]

class PublicDeploymentEndpoint(DeploymentEndpoint):

    """
    Publically exposed enpoint for CRUD on deployment model. Same
    thing as DeploymentEndpoint, but uses an API key for authentication instead of JWT.
    """
    authentication_classes = [APIKeyAuthentication]
    http_method_names = ['get'] # currently all CRUD needs to happen on the frontend, even if owner
    # lookup_field='data_uuid'

    def get_serializer_class(self):
        
        if self.request.method == 'GET':
            if self.request.user.is_staff:
                return DeploymentGETSerializer
            else:
                return PublicDeploymentGETSerializer
        else:
            return DeploymentSerializer


