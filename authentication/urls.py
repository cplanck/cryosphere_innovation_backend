from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from authentication.endpoints import *

# from general.endpoints import *

urlpatterns = [

    # non-social auth user creation
    path('user/create', CreateNewUser.as_view(), name='create new user'),

    # standard login endpoint
    path('login/', StandardLogin.as_view(),
         name='standard_user_login'),

    # google one-tap social login endpoint
    path('google/login/', GoogleOneTap.as_view(), name='google_onetap_login'),

    # refresh HTTP-only access-token if refresh is valid
    path('token/refresh', RefreshAccessToken.as_view(),
         name='refresh_access_token'),

    path('logout/', LogoutUser.as_view(), name='logout_user'),
]
