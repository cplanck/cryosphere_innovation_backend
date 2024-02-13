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
from .serializers import *




class NotificationEndpoint(viewsets.ModelViewSet):

    """
    Fetch notifications for a user
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieTokenAuthentication]

    def create(self, request):
        if request.data['user_saw_notifications']:
            notifications_to_update = Notification.objects.filter(for_user=request.user, seen=False)
            print(notifications_to_update)
            notifications_to_update.update(seen=True)
            return Response(f'Labeld {notifications_to_update.count()} notifications as seen')
        else:
            return super().create(request)

    def get_queryset(self):
        queryset = Notification.objects.filter(for_user=self.request.user).filter(deleted=False).order_by('seen').order_by('-date_added')

        return queryset
    
        
        