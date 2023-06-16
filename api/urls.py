
from django.urls import include, path
from rest_framework import routers

from api.endpoints import *

router = routers.DefaultRouter()

router.register('instruments', InstrumentEndpoint, basename='instruments')
router.register('deployments', DeploymentEndpoint, basename='deployments')

urlpatterns = [
    path('', include(router.urls)),
]
