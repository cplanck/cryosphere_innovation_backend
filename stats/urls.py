from django.urls import include, path
from rest_framework import routers

from stats.endpoints import *

router = routers.DefaultRouter()

# router.register('deployment-download-summary', DeploymentDownloadStatsSummaryEndpoint,
#                 basename='downloaded-deployments-summary-by-deployment')

router.register('deployment-download', DeploymentDownloadEndpoint,
                basename='downloaded-deployments')

router.register('admin', AdminStatsEndpoint,
                basename='admin-stats')

urlpatterns = [
    path('', include(router.urls)),
]
