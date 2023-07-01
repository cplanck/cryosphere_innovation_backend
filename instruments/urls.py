
from django.urls import include, path
from rest_framework import routers

from instruments.endpoints import *

router = routers.DefaultRouter()

router.register('instruments', InternalInstrumentEndpoint,
                basename='internal_instruments')

router.register('deployments', InternalDeploymentEndpoint,
                basename='internal_deployments')

router.register('deployment/data', InternalDataEndpoint, basename='my-api')


router.register('simb3_instrument_migration',
                SIMB3MigrationEndpoint, basename='new_data_endpoint')

router.register('simb3_deployment_migration',
                SIMB3DeploymentMigrationEndpoint, basename='simb3_deployment_migration')


urlpatterns = [
    path('', include(router.urls)),
]
