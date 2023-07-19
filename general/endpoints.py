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

from general.models import CustomerQuote, UpdatesAndChanges
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
    queryset = UpdatesAndChanges.objects.all().order_by('-published_date')
    serializer_class = UpdatesAndChangesSerializer
    authentication_classes = [CookieTokenAuthentication]


class CustomerQuoteEndpoint(viewsets.ModelViewSet):
    """
    This will need to be modified to allow for admin vs. user access
    """
    queryset = CustomerQuote.objects.all().order_by('-date_added')
    serializer_class = CustomerQuoteSerializer
    authentication_classes = [CookieTokenAuthentication]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.queryset.filter(user=self.request.user)
        else:
            return self.queryset.all()
