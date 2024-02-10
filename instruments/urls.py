
from django.urls import include, path
from rest_framework import routers
from django.http import HttpResponseRedirect
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
router.register('sensors/predict', PredictSensorFields,
                basename='predict_sensor_fields')
router.register('sensors', InstrumentSensorPackageEndpoint,
                basename='instrument_sensor_package')
router.register('add-unique-index', AddUniqueIDtoDeploymentMongoDB,
                basename='add_unique_index')

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

def api_root_page(request):
    return HttpResponseRedirect(os.getenv('STANDALONE_FRONTEND_ROOT') + '/docs/rest-api')

urlpatterns = [
    path('', api_root_page),
    path('', include(router.urls)),
]
