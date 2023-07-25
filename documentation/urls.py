from django.urls import include, path
from rest_framework import routers

from documentation.endpoints import *

router = routers.DefaultRouter()

router.register('images', DocumentImageEndpoint,
                basename='documentation_images')

router.register('', DocumentEndpoint,
                basename='document')


urlpatterns = [
    path('', include(router.urls)),
]
