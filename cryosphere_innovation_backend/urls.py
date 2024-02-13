from authentication.endpoints import *
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


urlpatterns = [
    path('', include('instruments.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('docs/', include('documentation.urls')),
    path('users/', include('user_profiles.urls')),
    path('general/', include('general.urls')),
    path('stats/', include('stats.urls')),
    path('real-time-data/', include('real_time_data.urls')),
    path('notifications/', include('notifications.urls')),
    path(r'rest-auth/', include('dj_rest_auth.urls')),
]
