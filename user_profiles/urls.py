from django.urls import include, path
from rest_framework import routers

from user_profiles.endpoints import *

router = routers.DefaultRouter()


router.register(r'', UserEndpoint, basename='users')
router.register(r'profile', UserProfileEndpoint, basename='user_profile')
router.register(r'settings', UserSettingsEndpoint,
                basename='user_settings')
router.register(r'profile/dashboard/watched_deployments',
                DashboardDeploymentMigration, basename='user_dashboard_instruments')
router.register(r'profile/dashboard/deployments',
                DashboardDeployments, basename='dashboard_deployments')

urlpatterns = [
    path('', include(router.urls)),
]
