
from django.urls import include, path
from rest_framework import routers

from instruments.endpoints import *
from instruments.public_endpoints import *
from instruments.user_endpoints import *

router = routers.DefaultRouter()

# Internal endpoints
# Used the the frontend
router.register('instruments', InstrumentEndpoint,
                basename='internal_instruments')
router.register('deployments', DeploymentEndpoint,
                basename='internal_deployments')
router.register('deployment/data', DeploymentDataEndpoint,
                basename='deployment_data')
router.register('sensors', InstrumentSensorPackageEndpoint,
                basename='instrument_sensor_package')

# User endpoints
# For the frontend user defined instruments/deployments
router.register('user/sensors', UserInstrumentSensorPackageEndpoint,
                basename='user_instrument_sensor_packages')
router.register('user/instruments', UserInstrumentEndpoint,
                basename='user_internal_instruments')
router.register('user/deployments', UserDeploymentEndpoint,
                basename='user_internal_deployments')
router.register('user/deployment/data', DeploymentDataEndpoint,
                basename='user_deployment_data')

# Public endpoints. 
# These use API key authentication
router.register('public/deployments', PublicDeploymentEndpoint, basename='public_deployment_endpoint')
router.register('public/deployment/data', PublicDataEndpoint, basename='public_data_endpoint')

urlpatterns = [
    path('', include(router.urls)),
]
