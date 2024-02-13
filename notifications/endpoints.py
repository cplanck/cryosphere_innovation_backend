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
import boto3
from botocore.exceptions import ClientError




class NotificationEndpoint(viewsets.ModelViewSet):

    """
    Fetch notifications for a user

    Written 13 Feb 2023
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieTokenAuthentication]

    def create(self, request):
        # Mark all notifications as seen
        if request.data['user_saw_notifications']:
            notifications_to_update = Notification.objects.filter(for_user=request.user, seen=False)
            notifications_to_update.update(seen=True)
            return Response(f'Labeld {notifications_to_update.count()} notifications as seen')
        else:
            return super().create(request)

    def get_queryset(self):
        queryset = Notification.objects.filter(for_user=self.request.user).filter(deleted=False).order_by('seen').order_by('-date_added')
        return queryset
    
def send_email_to_user():
    ses = boto3.client('ses', region_name='us-east-1')
    try:
        response = ses.send_email(
            Source='cjp@cryosphereinnovation.com',
            Destination={'ToAddresses': ['cjp@cryosphereinnovation.com']},
            Message={
                'Subject': {'Data': 'Hello Cameron'},
                'Body': {'Html': {'Data': '<div>Hello world</div>'}}
            }
        )
        return True

    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
        
class TestAmazonEmail(viewsets.ViewSet):

    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAdminUser]

    def create(self, request):
        send_email_to_user()
        return Response({'Email endpoint working'})