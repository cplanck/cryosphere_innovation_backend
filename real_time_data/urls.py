from django.urls import include, path
from rest_framework import routers

from real_time_data.endpoints import *

router = routers.DefaultRouter()

router.register('decode-scripts/preview', DecodeScriptPreviewEndpoint,
                basename='sbd_message_preview')

router.register('decode-scripts', DecodeScriptsEndpoint,
                basename='decode-scripts')

router.register('', RealTimeDataEndpoint,
                basename='real_time_data')

urlpatterns = [
    path('', include(router.urls)),
]
