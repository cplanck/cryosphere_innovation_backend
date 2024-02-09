import base64
import io
import json
import os
import shutil
import sys
import time as Time
from ast import Del
from time import time
from datetime import datetime

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
# from oauth2client import client, tools
# from oauth2client.file import Storage
import base64
from io import BytesIO

# from decode_scripts import decode_sbd, dynamic_decode

GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SERVICE_ACCOUNT_FILE = 'gmail_service_account_token.json'
DELEGATE = 'iridiumdata@cryosphereinnovation.com'

# Load service account credentials from file
gmail_creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=GMAIL_SCOPES
)
credentials_delegated = gmail_creds.with_subject(DELEGATE)
gmail_service = build('gmail', 'v1', credentials=credentials_delegated)

request = {
'labelIds': ['INBOX'],
'topicName': 'projects/cryosphere-innovation/topics/sbd-data-download-lambda-trigger'
}
gmail_service.users().watch(userId=DELEGATE, body=request).execute()

def get_binary_message_attachment(service, user_id, msg_id):
    
    """
    Given a message ID, retreive the full message from Gmail and return the data as a 
    binary object
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        for part in message['payload']['parts']:
            newvar = part['body']
            binary_object = None
            file_data = None
            file_name = None
            if 'attachmentId' in newvar:
                att_id = newvar['attachmentId']
                att = service.users().messages().attachments().get(
                    userId=user_id, messageId=msg_id, id=att_id).execute()
                data = att['data']
                file_data = base64.urlsafe_b64decode(data.encode())
                binary_object = io.BytesIO(file_data)
                file_name = part['filename']
            
        return binary_object, file_data, file_name
            
    except errors.HttpError as error:
        print('An error occurred: %s' % error)



# binary_message_object, base64_encoded_file, file_name = get_binary_message_attachment(gmail_service,'me', '10242187521676158')

# message = gmail_service.users().messages().get(userId='me', id='189eec565e48a9ef').execute()

samplePubSubMessage = {'version': '2.0', 'routeKey': '$default', 'rawPath': '/', 'rawQueryString': '', 'headers': {'content-length': '371', 'x-amzn-tls-version': 'TLSv1.2', 'x-forwarded-proto': 'https', 'x-forwarded-port': '443', 'x-forwarded-for': '66.102.9.98', 'accept': 'application/json', 'x-amzn-tls-cipher-suite': 'ECDHE-RSA-AES128-GCM-SHA256', 'x-amzn-trace-id': 'Root=1-65c5346a-12c9b97c2d3f77912277082b', 'host': 'aid6pluilxmnmikbpkya6yhw4a0klpim.lambda-url.us-east-1.on.aws', 'content-type': 'application/json', 'from': 'noreply@google.com', 'accept-encoding': 'gzip, deflate, br', 'user-agent': 'APIs-Google; (+https://developers.google.com/webmasters/APIs-Google.html)'}, 'requestContext': {'accountId': 'anonymous', 'apiId': 'aid6pluilxmnmikbpkya6yhw4a0klpim', 'domainName': 'aid6pluilxmnmikbpkya6yhw4a0klpim.lambda-url.us-east-1.on.aws', 'domainPrefix': 'aid6pluilxmnmikbpkya6yhw4a0klpim', 'http': {'method': 'POST', 'path': '/', 'protocol': 'HTTP/1.1', 'sourceIp': '66.102.9.98', 'userAgent': 'APIs-Google; (+https://developers.google.com/webmasters/APIs-Google.html)'}, 'requestId': 'e98c91d6-424b-44ad-993c-622bf999c846', 'routeKey': '$default', 'stage': '$default', 'time': '08/Feb/2024:20:07:06 +0000', 'timeEpoch': 1707422826131}, 'body': '{"message":{"data":"eyJlbWFpbEFkZHJlc3MiOiJpcmlkaXVtZGF0YUBjcnlvc3BoZXJlaW5ub3ZhdGlvbi5jb20iLCJoaXN0b3J5SWQiOjU5MjA1NTl9","messageId":"10242339755584202","message_id":"10242339755584202","publishTime":"2024-02-08T20:07:04.706Z","publish_time":"2024-02-08T20:07:04.706Z"},"subscription":"projects/cryosphere-innovation/subscriptions/sbd-data-download-lambda-trigger-sub"}\n', 'isBase64Encoded': False}

samplePubSubMessage = {'data':{'emailAddress': 'iridiumdata@cryosphereinnovation.com', 'historyId': 5928978}}

DELEGATE = 'iridiumdata@cryosphereinnovation.com'

# Load service account credentials from file
gmail_creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=GMAIL_SCOPES
)
credentials_delegated = gmail_creds.with_subject(DELEGATE)
gmail_service = build('gmail', 'v1', credentials=credentials_delegated)

request = {
    'labelIds': ['INBOX'],
    'topicName': 'projects/cryosphere-innovation/topics/sbd-data-download-lambda-trigger',
    'historyTypes': ['messageAdded'],
}

# Execute watch request on Gmail inbox
r = gmail_service.users().watch(userId=DELEGATE, body=request).execute()
print(r)


# def get_email_from_pub_sub_body(history_id):

#     """
#     Takes a historyId from a Gmail Pub/Sub subscription and fetchs the email that triggered the event
#     by looking at the messagesAdded event. 
#     """
#     # Fetch the history record using the history ID
#     history_record = gmail_service.users().history().list(userId='me', startHistoryId=history_id).execute()

#     # print(history_record)

#     if 'history' in history_record:
#         message_id = history_record['history'][0]['messages'][0]['id']
#     # print(history_record['history'])
#     # message_added = next((d for d in history_record['history'] if 'messagesAdded' in d), None)
#     # print('MESSAGE ADDED', message_added['messages'][0]['id'])
#     # message_id = message_added['messages'][0]['id']
#     # message_added = next((d for d in history_record['history'] if 'messagesAdded' in d), None)



#     email_message = gmail_service.users().messages().get(userId='me', id=message_id).execute()
#     subject_dict = next((d for d in email_message['payload']['headers'] if d.get('name') == 'Subject'), None)
#     print(subject_dict)
#     # Next: fetch data for this id if message == SBD...

def get_gmail_from_pub_sub_body(history_id):

    """
    Takes a historyId from a Gmail Pub/Sub subscription and fetchs the email that triggered the event
    by looking at the messagesAdded event. 
    """
    
    # Fetch the history record using the history ID
    history_record = gmail_service.users().history().list(userId='me', startHistoryId=history_id).execute()

    # print(history_record['history'])
    # message_added = next((d for d in history_record['history'] if 'messagesAdded' in d), None)
    # message_id = message_added['messages'][0]['id']

    if 'history' in history_record:
        message_id = history_record['history'][0]['messages'][0]['id']
        
    email_message = gmail_service.users().messages().get(userId='me', id=message_id).execute()
    subject_dict = next((d for d in email_message['payload']['headers'] if d.get('name') == 'Subject'), None)

    return email_message, subject_dict, message_id

# email_message, subject_dict, message_id = get_gmail_from_pub_sub_body('5928576')   

# print(email_message)
# print(subject_dict['value'])
# print(message_id)






# data_string_from_pub_sub = 'eyJlbWFpbEFkZHJlc3MiOiJpcmlkaXVtZGF0YUBjcnlvc3BoZXJlaW5ub3ZhdGlvbi5jb20iLCJoaXN0b3J5SWQiOjU5MjIyODh9'
# decoded_data_string = base64.b64decode(data_string_from_pub_sub).decode('utf-8')

# print(decoded_data_string)
# history_id = json.loads(decoded_data_string)['historyId']

# try:
#     get_email_from_pub_sub_body(history_id)
# except Exception as e:
#     print(e)
#     print('No new message')