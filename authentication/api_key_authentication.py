import jwt
from django.conf import settings
from django.contrib.auth.models import User
from dotenv import load_dotenv
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from authentication.models import APIKey
from instruments.models import Deployment
from rest_framework import permissions

load_dotenv()

class APIKeyAuthentication(BaseAuthentication):

    """
    API key authentication class. Simply checks if an 
    API key was passed in the header, identifying the user
    if it is and rejecting the request if it isn't. 
    """

    def authenticate(self, request):
        api_key = request.META.get('HTTP_AUTHENTICATION') or request.META.get('AUTHENTICATION')
        if not api_key:
            raise AuthenticationFailed(f'Missing API key.')
        
        api_key_obj = APIKey.objects.get(key=api_key)
        if request.method not in permissions.SAFE_METHODS and api_key_obj.read_only:
                raise AuthenticationFailed(f'Your read-only API key does not give you write access to this data.')
        else:
            user = api_key_obj.user
            return (user, None)
        
        # except Exception as e:
        #     print(e)
        #     raise AuthenticationFailed(f'There was a problem authenticating your your request. It is possible that you have a badly formatted API key.')
       