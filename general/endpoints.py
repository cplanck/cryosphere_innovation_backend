import json

from authentication.http_cookie_authentication import CookieTokenAuthentication
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
from instruments.models import Deployment, Instrument, InstrumentSensorPackage
from rest_framework import pagination, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import (AllowAny, BasePermission, IsAdminUser,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from general.models import *
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

        return Response('It worked!')


class UpdatesAndChangesEndpoint(viewsets.ModelViewSet):
    queryset = UpdatesAndChanges.objects.order_by('-published_date')
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


class BannerEndpoint(viewsets.ModelViewSet):
    queryset = Banner.objects.all().order_by('-date_added')
    serializer_class = BannerSerializer
    authentication_classes = [CookieTokenAuthentication]


class UserSurveyEndpoint(viewsets.ModelViewSet):
    queryset = UserSurvey.objects.all().order_by('-date_added')
    serializer_class = UserSurveySerializer


class ContactUsEndpoint(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all().order_by('-date_added')
    serializer_class = ContactUsSerializer


class AdminInfoEndpoint(viewsets.ViewSet):
    def list(self, request):
        deployments = Deployment.objects.count()
        instruments = Instrument.objects.count()
        users = User.objects.count()
        sensor_packages = InstrumentSensorPackage.objects.count()
        unseen_contact_forms = ContactUs.objects.filter(seen=False).count()
        user_survey_count = UserSurvey.objects.count()
        response = {'deployments': deployments,
                    'instruments': instruments, 'users': users, 'sensor_packages': sensor_packages, 'unseen_contact_forms': str(unseen_contact_forms), 'user_survey_count': str(user_survey_count)}
        return Response(response, status=status.HTTP_200_OK)
