from django.urls import include, path
from rest_framework import routers

from general.endpoints import *

router = routers.DefaultRouter()

router.register('changelog', UpdatesAndChangesEndpoint, basename='changelog')
router.register('quote', CustomerQuoteEndpoint, basename='quote')
router.register('banner', BannerEndpoint, basename='banner')
router.register('user_survey', UserSurveyEndpoint, basename='user_survey')

urlpatterns = [
    path('', include(router.urls)),
    path('test_email', SendUserEmail.as_view())
]
