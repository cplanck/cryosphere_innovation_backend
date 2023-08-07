from django.urls import include, path
from rest_framework import routers

from real_time_data.endpoints import *

router = routers.DefaultRouter()

router.register('', RealTimeDataEndpoint,
                basename='real_time_data')

urlpatterns = [
    path('', include(router.urls)),
]
