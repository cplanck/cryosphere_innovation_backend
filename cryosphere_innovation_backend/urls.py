from authentication.endpoints import *
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from rest_framework.documentation import include_docs_urls


def index(request):
    return HttpResponse("")


urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('api/', include('instruments.urls')),
    path('articles/', include('articles.urls')),
    path('data/', include('data.urls')),
    path('users/', include('user_profiles.urls')),
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('docs/', include_docs_urls(title='api')),
]
