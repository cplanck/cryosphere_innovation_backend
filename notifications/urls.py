
from django.urls import include, path
from rest_framework import routers
from .endpoints import *

router = routers.DefaultRouter()

router.register('', NotificationEndpoint,
                basename='notifications')

urlpatterns = [
    path('', include(router.urls)),
]
