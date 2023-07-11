from django.urls import include, path
from rest_framework import routers

from general.endpoints import *

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('test_email', SendUserEmail.as_view())
]
