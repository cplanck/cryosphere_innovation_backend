from django.urls import include, path
from rest_framework import routers

from articles import views as article_views
from articles.endpoints import *

router = routers.DefaultRouter()

router.register('', ArticleEndpoint,
                basename='articles')

urlpatterns = [
    path('', include(router.urls)),
]
