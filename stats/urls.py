from django.urls import include, path
from rest_framework import routers

from stats.endpoints import *

router = routers.DefaultRouter()

router.register('deployment-download', DeploymentDownloadEndpoint,
                basename='downloaded-deployments')

urlpatterns = [
    path('', include(router.urls)),
]
