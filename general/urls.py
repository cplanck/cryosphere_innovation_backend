from django.urls import include, path
from rest_framework import routers

from general.endpoints import *

router = routers.DefaultRouter()

router.register('changelog', UpdatesAndChangesEndpoint, basename='changelog')
router.register('quote', CustomerQuoteEndpoint, basename='quote')
router.register('banner', BannerEndpoint, basename='banner')
router.register('user_survey', UserSurveyEndpoint, basename='user_survey')
router.register('contact_us', ContactUsEndpoint, basename='contact_us')
router.register('status', WebsiteStatusEndpoint, basename='website_status')
router.register('admin', AdminInfoEndpoint, basename='admin_endpoint')

urlpatterns = [
    path('', include(router.urls)),
    path('test_email', SendUserEmail.as_view())
]
