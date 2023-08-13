import jwt
from django.conf import settings
from django.contrib.auth.models import User
from dotenv import load_dotenv
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

load_dotenv()


class CookieTokenAuthentication(BaseAuthentication):

    """
    Authenticate a user using http cookies recieved from the browser. 
    The cookie access_token is required for authentication. 

    Written 12 July 2023
    """
    def authenticate(self, request):
        access_token = self.get_token_from_cookie(request)

        if not access_token:
            return None
        try:
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidTokenError:
            return None
            # raise AuthenticationFailed('Invalid token')

        user_id = payload.get('user_id')

        if not user_id:
            raise AuthenticationFailed('Missing user_id in token payload')

        user = User.objects.get(id=user_id)

        return (user, access_token)

    def get_token_from_cookie(self, request):
        access_token = None

        if 'access_token' in request.COOKIES:
            access_token = request.COOKIES['access_token']

        return access_token
