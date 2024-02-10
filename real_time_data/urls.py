from django.urls import include, path
from rest_framework import routers

from real_time_data.endpoints import *

router = routers.DefaultRouter()

router.register('sbd_gmail_pub_sub', SBDGmailPubSubEndpoint,
                basename='sbd_gmail_pub_sub')

router.register('sbd_data_download_by_imei', SBDDataDownloadEndpoint,
                basename='sbd_data_download_by_imei')

router.register('decode-sbd-binary', SBDDecodeBinary,
                basename='decode_sbd_binary')

router.register('sbd-details', GetSBDDetailsByDeployment,
                basename='sbd-details')

router.register('decode-scripts/preview', DecodeScriptPreviewEndpoint,
                basename='sbd_message_preview')

router.register('decode-scripts', DecodeScriptsEndpoint,
                basename='decode-scripts')

router.register('', RealTimeDataEndpoint,
                basename='real_time_data')

urlpatterns = [
    path('', include(router.urls)),
]
