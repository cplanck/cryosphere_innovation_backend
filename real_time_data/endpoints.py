from authentication.http_cookie_authentication import CookieTokenAuthentication
from authentication.models import APIKey
from rest_framework import pagination, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import (AllowAny, BasePermission, IsAdminUser,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction
from django.http import JsonResponse
import datetime
import json
import base64
import boto3
import httplib2
import requests
from apiclient import discovery, errors
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from io import BytesIO
import io
from .binaryreader import *
import collections
from instruments.base_models import InstrumentSensorPackage
from .models import RealTimeData, DecodeScript
from .serializers import (RealTimeDataSerializer, RealTimeDataPOSTSerializer, DecodeScriptSerializer)
from django.http.request import QueryDict
import os
from real_time_data.models import *
import pickle
import time
import pytz

GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


if os.getenv('WEBSITE_ROOT') == 'http://localhost:8000':
    SERVICE_ACCOUNT_FILE = 'gmail_service_account_token.json'
else:
    SERVICE_ACCOUNT_FILE = '/home/cplanck/cryosphere_innovation_backend/gmail_service_account_token.json'

DELEGATE = 'iridiumdata@cryosphereinnovation.com'

gmail_creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=GMAIL_SCOPES
)
credentials_delegated = gmail_creds.with_subject(DELEGATE)
gmail_service = build('gmail', 'v1', credentials=credentials_delegated)

class RealTimeDataEndpoint(viewsets.ModelViewSet):

    """
    Endpoint for CRUD on the real-time data model. This model
    is used my the AWS lambda function to control what and how
    deployments get decoded, posted to the DB, etc. 
    """

    authentication_classes = [CookieTokenAuthentication]
    queryset = RealTimeData.objects.all().order_by('-last_modified')
    serializer_class = RealTimeDataSerializer
    filterset_fields = ['active']

    def get_serializer_class(self):
        
        if self.request.method == 'GET':
           
            return RealTimeDataSerializer
        else:
            return RealTimeDataPOSTSerializer

class DecodeScriptsEndpoint(viewsets.ModelViewSet):

    """
    Endpoint for CRUD on the decode-script model. The decode-scripts
    dynamically define Python functions which are used by the Lambda
    functions for decoding SBD binary files.  
    """

    authentication_classes = [CookieTokenAuthentication]
    queryset = DecodeScript.objects.all().order_by('-last_modified')
    serializer_class = DecodeScriptSerializer


class DecodeScriptPreviewEndpoint(viewsets.ViewSet):

    def create(self, request):
        binary_file = request.FILES.get('file')
        decode_script_id = request.data['decode_script_id']
        print(decode_script_id)

        if binary_file:
            try:
                sbd_message_bytes = BinaryReader(binary_file)
                script = DecodeScript.objects.get(id=decode_script_id)
                if not script.script:
                    return JsonResponse({'error': 'No decode script found'}, status=400)
                
                data = collections.OrderedDict()
                compiled_script = compile(script.script, "filename", "exec")
                exec(compiled_script)
                return Response({'decoded_message':data})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

    authentication_classes = [CookieTokenAuthentication]

def get_gmail_from_pub_sub_body(history_id):

    """
    Takes a historyId from a Gmail Pub/Sub subscription and fetchs the email that triggered the event
    by looking at the messagesAdded event. 
    """

    # delay necessary to wait for Gmail to land after Pub/Sub request
    time.sleep(5)
    
    # Fetch the history record using the history ID
    history_record = gmail_service.users().history().list(userId='me', startHistoryId=history_id).execute()

    print('HISTORY RECORD: ', history_record)

    if 'history' in history_record:
        message_id = history_record['history'][0]['messages'][0]['id']

    email_message = gmail_service.users().messages().get(userId='me', id=message_id).execute()
    subject_dict = next((d for d in email_message['payload']['headers'] if d.get('name') == 'Subject'), None)

    return email_message, subject_dict, message_id
    # Next: fetch data for this id if message == SBD...


def get_recent_gmails(seconds_ago=60):

    pacific_timezone = pytz.timezone('US/Pacific')
    current_time_utc = datetime.datetime.utcnow()
    current_time_pacific = current_time_utc.astimezone(pacific_timezone)
    time_600_seconds_ago = current_time_pacific - datetime.timedelta(seconds=seconds_ago)
    unix_timestamp = int(time_600_seconds_ago.timestamp())

    # Define the search query
    search_query = f'after:{unix_timestamp}'
    print(search_query)

    response = gmail_service.users().messages().list(userId='me', q=search_query).execute()
    return response


def get_binary_message_attachment(msg_id):
    
    """
    Given a message ID, retreive the full message from Gmail and return the data as a 
    binary object
    """
    try:
        message = gmail_service.users().messages().get(userId='me', id=msg_id).execute()

        for part in message['payload']['parts']:
            newvar = part['body']
            binary_object = None
            file_data = None
            file_name = None
            if 'attachmentId' in newvar:
                att_id = newvar['attachmentId']
                att = gmail_service.users().messages().attachments().get(
                    userId='me', messageId=msg_id, id=att_id).execute()
                data = att['data']
                file_data = base64.urlsafe_b64decode(data.encode())
                binary_object = io.BytesIO(file_data)
                file_name = part['filename']
            
        return binary_object, file_name
            
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None

def get_gmail_from_message_id(message_id):

    """
    Takes a valid Gmail message_id and fetchs the full email, subject, and attachement
    """

    try:
        email_message = gmail_service.users().messages().get(userId='me', id=message_id).execute()
        subject = next((d for d in email_message['payload']['headers'] if d.get('name') == 'Subject'), None)

        if subject and len(subject['value']) >= 18 and subject['value'][:18] == 'SBD Msg From Unit:':
            # SBD message found
            binary_message_object, file_name = get_binary_message_attachment(message_id)
            imei = file_name[:15]
            return binary_message_object, file_name, imei
    except:
        print('There was a problem fetching the gmail')
        return None


def create_sbd_data_entry_from_gmail_and_deployment(binary_message_object, file_name, deployment):
    try:
        with transaction.atomic():
            sbd_data_object = SBDData(deployment=deployment, sbd_filename=file_name, sbd_binary=binary_message_object.getvalue())
            sbd_data_object.save()
            return True 
    except Exception as e:
        print("Error occurred while saving SBD data entry:", e)
        return False

        


# class SBDGmailPubSubEndpoint(viewsets.ViewSet):

#     def create(self, request):

#         """
#         Takes a POST request from the Gmail Pub/Sub and extracts the email that caused the 
#         Pub/Sub trigger. 

#         Note: this endpoint must return an OK (~200) status code or the Gmail Pub/Sub endpoint
#         will continue to retry. 

#         Written 8 Feb 2024
#         """

#         print('INSIDE GMAIL PUB SUB ENDPOINT')

#         try:
#             if not request.content_type or request.content_type == '':
#                     request.META['CONTENT_TYPE'] = 'application/json'
            
#             print(request.data)
#             pub_sub_history_id = request.data['historyId']
#             email, subject, message_id = get_gmail_from_pub_sub_body(pub_sub_history_id)

#             print('EMAIL: ', email)
#             print('SUBJECT ', subject)
            
#             if subject and len(subject['value']) >= 18 and subject['value'][:18] == 'SBD Msg From Unit:':
#                 print('SBD MESSAGE RECEIVED')
#                 # message is (likely) from Iridium (note: only checking the subject, not the sender)
#                 binary_message_object, file_name = get_binary_message_attachment(message_id)
#                 imei = file_name[:15]
#                 print(imei)

#                 # Take the first RTD object if there are multiple for an IMEI
#                 real_time_data_object = RealTimeData.objects.filter(iridium_imei=imei).first()

#                 # extract binary file if it exists
#                 # associate an active Real-time data object
#                 # decode using Lambda function
#                 # store file on S3 and in database
#                 # post to mongodb
#                 if binary_message_object:
#                     print('BINARY MESSAGE FOUND:')
#                     print(binary_message_object)
#                     if real_time_data_object:
#                         print('Real time data object found for this IMEI:')
#                         try:
#                             sbd_data_object = SBDData(deployment=real_time_data_object.deployment, sbd_filename=file_name, sbd_binary=binary_message_object.getvalue())
#                             sbd_data_object.save()
#                             # sample = SBDData.objects.get(deployment=real_time_data_object.deployment)
#                             # print(sample.deployment)
#                             # # print(sample.sbd_binary.tobytes())

#                             # byte_data = sample.sbd_binary.tobytes()
#                             # for byte in byte_data:
#                             #     print('{:02x}'.format(byte))

#                             # print(sample.sbd_filename)
#                         except Exception as e:
#                             print(e)

#                 return JsonResponse({'subject': subject, 'email': email}, status=200)
#             else:
#                 return Response({}, status=200)
#         except Exception as e:
#             print('Error, likely no message ID found: ', e)
#             return Response({}, status=200)
    
class SBDGmailPubSubEndpoint(viewsets.ViewSet):

    def create(self, request):

        """
        Endpoint attached to the Gmail Pub/Sub push endpoint. 
        Gmail doesnt bake in email data to the pub/sub endpoint, so we 
        simply poll the inbox and loop through all messages that arrived in 
        the last 5 seconds when theres a notification of a change.

        Written 8 Feb 2024
        """

        print('INSIDE NEW GMAIL PUB SUB ENDPOINT')

        if not request.content_type or request.content_type == '':
                request.META['CONTENT_TYPE'] = 'application/json'
        
        # print(request.data)
        # pub_sub_history_id = request.data['historyId']
        # email, subject, message_id = get_gmail_from_pub_sub_body(pub_sub_history_id)
        # binary_message_object, file_name, imei = get_gmail_from_message_id(message_id)
        # print(file_name)

        # time.sleep(5)
                
        try:
            recent_email_list = get_recent_gmails(30)
        except Exception as e:
            # if no recent messages are found, return a 400 so Pub/Sub tries again
            return Response('No message found', status=400)
        
        print(recent_email_list)
        if 'messages' in recent_email_list:
            for message in recent_email_list['messages']:
                print(message['id'])
                try:
                    binary_message_object, file_name, imei = get_gmail_from_message_id(message['id'])
                    real_time_data_object = RealTimeData.objects.filter(iridium_imei=imei).first()
                    if real_time_data_object:
                        print('REAL TIME DATA OBJECT FOUND')
                        sbd_data_object = SBDData(deployment=real_time_data_object.deployment, sbd_filename=file_name, sbd_binary=binary_message_object.getvalue())
                        sbd_data_object.save()   
                    print(file_name)
                    print(imei)
                except Exception as e:
                    print(e)
                    print('There was a problem retreiving the email or creating the SBD data object')

        return Response({}, status=200)

            # binary_message_object, file_name, imei = get_gmail_from_message_id()
            
        #     if subject and len(subject['value']) >= 18 and subject['value'][:18] == 'SBD Msg From Unit:':
        #         print('SBD MESSAGE RECEIVED')
        #         # message is (likely) from Iridium (note: only checking the subject, not the sender)
        #         binary_message_object, file_name = get_binary_message_attachment(message_id)
        #         imei = file_name[:15]
        #         print(imei)

        #         # Take the first RTD object if there are multiple for an IMEI
        #         real_time_data_object = RealTimeData.objects.filter(iridium_imei=imei).first()

        #         # extract binary file if it exists
        #         # associate an active Real-time data object
        #         # decode using Lambda function
        #         # store file on S3 and in database
        #         # post to mongodb
        #         if binary_message_object:
        #             print('BINARY MESSAGE FOUND:')
        #             print(binary_message_object)
        #             if real_time_data_object:
        #                 print('Real time data object found for this IMEI:')
        #                 try:
        #                     sbd_data_object = SBDData(deployment=real_time_data_object.deployment, sbd_filename=file_name, sbd_binary=binary_message_object.getvalue())
        #                     sbd_data_object.save()
        #                     # sample = SBDData.objects.get(deployment=real_time_data_object.deployment)
        #                     # print(sample.deployment)
        #                     # # print(sample.sbd_binary.tobytes())

        #                     # byte_data = sample.sbd_binary.tobytes()
        #                     # for byte in byte_data:
        #                     #     print('{:02x}'.format(byte))

        #                     # print(sample.sbd_filename)
        #                 except Exception as e:
        #                     print(e)

        #         return JsonResponse({'subject': subject, 'email': email}, status=200)
        #     else:
        #         return Response({}, status=200)
        # except Exception as e:
        #     print('Error, likely no message ID found: ', e)
        #     return Response({}, status=200)
        

class SBDDataDownloadEndpoint(viewsets.ViewSet):

    """
    - Takes an IMEI in a POST request
    - Checks if its registered for Real-Time Data
    - If it is, it gets all the messages in the Gmail inbox that match the IMEI
    - Then it downloads the emails and creates an SBDdata entry for each file
    - Returns the number of saved SBDData entries
    """

    def create(self, request):

        imei = request.data['imei']
        real_time_data_object = RealTimeData.objects.filter(iridium_imei=imei).first()

        if real_time_data_object:
            try:
                subject = 'subject: sbd msg from unit: {}'.format(request.data['imei'])
                response = gmail_service.users().messages().list(
                    userId='me', maxResults=500, q=subject).execute()

                messages = []
                if 'messages' in response:
                    messages.extend(response['messages'])

                while 'nextPageToken' in response:
                    page_token = response['nextPageToken']
                    response = gmail_service.users().messages().list(userId='me', maxResults=500,
                                                            q=subject, pageToken=page_token).execute()
                    if 'messages' in response:
                        messages.extend(response['messages'])
            
            except Exception as e:
                print('There was a problem downloading messages')
                return Response({})
        else:
            return Response({'Real-time data isnt set up for this IMEI'})
        
        saved_entries = 0
        print('MESSAGES LENGTH: ', messages)

        for message in messages:
            binary_message_object, file_name, imei = get_gmail_from_message_id(message['id'])
            print(file_name)
            save_successful = create_sbd_data_entry_from_gmail_and_deployment(binary_message_object, file_name, real_time_data_object.deployment)

            if save_successful:
                saved_entries = saved_entries + 1
        
        return Response({'saved_entries': saved_entries})