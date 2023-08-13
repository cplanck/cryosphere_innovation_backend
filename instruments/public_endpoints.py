from authentication.api_key_authentication import APIKeyAuthentication
from .endpoints import DeploymentDataEndpoint, DeploymentEndpoint

class PublicDataEndpoint(DeploymentDataEndpoint):

    """
    Publically exposed enpoint for CRUD on deployment data. Same
    thing as DeploymentDataEndpoint, but uses an API key for authentication.
    """
    authentication_classes = [APIKeyAuthentication]

class PublicDeploymentEndpoint(DeploymentEndpoint):

    """
    Publically exposed enpoint for CRUD on deployment model. Same
    thing as DeploymentEndpoint, but uses an API key for authentication.
    """
    authentication_classes = [APIKeyAuthentication]
    http_method_names = ['get'] # all CRUD needs to happen on the frontend, even if owner


