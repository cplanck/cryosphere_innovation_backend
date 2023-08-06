
from django.urls import include, path
from rest_framework import routers

from instruments.endpoints import *
from instruments.user_endpoints import *

router = routers.DefaultRouter()

router.register('instruments', InternalInstrumentEndpoint,
                basename='internal_instruments')

router.register('deployments', InternalDeploymentEndpoint,
                basename='internal_deployments')

router.register('deployment/data', InternalDataEndpoint,
                basename='deployment_data')

### endpoints for user defined instruments/deployments ###
router.register('user/sensors', UserInstrumentSensorPackageEndpoint,
                basename='user_instrument_sensor_packages')
            
router.register('user/instruments', UserInstrumentEndpoint,
                basename='user_internal_instruments')

router.register('user/deployments', UserDeploymentEndpoint,
                basename='user_internal_deployments')

router.register('user/deployment/data', UserDataEndpoint,
                basename='user_deployment_data')
########################################################

router.register('sensors', InstrumentSensorPackageEndpoint,
                basename='instrument_sensor_package')

router.register('simb3_instrument_migration',
                SIMB3MigrationEndpoint, basename='new_data_endpoint')

router.register('simb3_deployment_migration',
                SIMB3DeploymentMigrationEndpoint, basename='simb3_deployment_migration')


urlpatterns = [
    path('', include(router.urls)),
]
