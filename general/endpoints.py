from authentication.http_cookie_authentication import CookieTokenAuthentication
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework import pagination, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import (AllowAny, BasePermission, IsAdminUser,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from general.models import UpdatesAndChanges
from general.serializers import *


class SendUserEmail(APIView):

    def get(self, request):
        send_mail(
            'Subject here',
            'Here is the message.',
            'support@cryosphereinnovation.com',
            ['cinvtestpage@gmail.com'],
            fail_silently=False,
        )

        return Response('I worked!')


class UpdatesAndChangesEndpoint(viewsets.ModelViewSet):
    queryset = UpdatesAndChanges.objects.all()
    serializer_class = UpdatesAndChangesSerializer
    # permission_classes = [CookieTokenAuthentication]
