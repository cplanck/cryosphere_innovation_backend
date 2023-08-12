import jwt
from django.conf import settings
from django.contrib.auth.models import User
from dotenv import load_dotenv
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from authentication.models import APIKey
from instruments.models import Deployment

load_dotenv()

class APIKeyAuthentication(BaseAuthentication):

    """
    API key authentication class. Simply checks if an 
    API key was passed in the header, identifying the user
    if it is and rejecting the request if it isn't. 
    """

    def authenticate(self, request):
        api_key = request.META.get('HTTP_AUTHENTICATION')
        if not api_key:
            raise AuthenticationFailed(f'Missing API key.')
        try:
            api_key_obj = APIKey.objects.get(key=api_key)
            user = api_key_obj.user
            return (user, None)
        except Exception as e:
            raise AuthenticationFailed(f'You do not have access to this data.')
       