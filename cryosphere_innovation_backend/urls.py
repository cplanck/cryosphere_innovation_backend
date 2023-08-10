from authentication.endpoints import *
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.urls import include, path
from rest_framework.documentation import include_docs_urls


def index(request):
    return HttpResponse("")


urlpatterns = [
    path('', include('instruments.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('docs/', include('documentation.urls')),
    path('data/', include('data.urls')),
    path('users/', include('user_profiles.urls')),
    path('general/', include('general.urls')),
    path('stats/', include('stats.urls')),
    path('real-time-data/', include('real_time_data.urls')),
    path(r'rest-auth/', include('dj_rest_auth.urls')),
]
