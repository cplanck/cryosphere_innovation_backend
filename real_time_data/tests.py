from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from data.mongodb import delete_mongodb_collection

from instruments.models import Deployment, Instrument
from authentication.models import APIKey


class TestSBDPubSubPostRequest(APITestCase):
    
    """    
    Test for initiating decoding when a POST request is made from the Gmail inbox. 

    RUN THESE TESTS WITH:
    python3 manage.py test real_time_data.tests.test_sbd_pub_sub_post_request --keepdb
    """

    def test_sbd_pub_sub_post_request(self):

        sample_pub_sub_payload = {'version': '2.0', 'routeKey': '$default', 'rawPath': '/', 'rawQueryString': '', 'headers': {'content-length': '75', 'x-amzn-tls-version': 'TLSv1.2', 'x-goog-pubsub-publish-time': '2024-02-08T23:26:38.252Z', 'x-forwarded-proto': 'https', 'x-goog-pubsub-subscription-name': 'projects/cryosphere-innovation/subscriptions/sbd-data-download-lambda-trigger-sub', 'x-forwarded-port': '443', 'x-forwarded-for': '66.102.9.103', 'accept': 'application/json', 'x-goog-pubsub-message-id': '10242257573869679', 'x-amzn-tls-cipher-suite': 'ECDHE-RSA-AES128-GCM-SHA256', 'x-amzn-trace-id': 'Root=1-65c5632e-03a3b292386b7aeb345ae363', 'host': 'aid6pluilxmnmikbpkya6yhw4a0klpim.lambda-url.us-east-1.on.aws', 'from': 'noreply@google.com', 'accept-encoding': 'gzip, deflate, br', 'user-agent': 'APIs-Google; (+https://developers.google.com/webmasters/APIs-Google.html)'}, 'requestContext': {'accountId': 'anonymous', 'apiId': 'aid6pluilxmnmikbpkya6yhw4a0klpim', 'domainName': 'aid6pluilxmnmikbpkya6yhw4a0klpim.lambda-url.us-east-1.on.aws', 'domainPrefix': 'aid6pluilxmnmikbpkya6yhw4a0klpim', 'http': {'method': 'POST', 'path': '/', 'protocol': 'HTTP/1.1', 'sourceIp': '66.102.9.103', 'userAgent': 'APIs-Google; (+https://developers.google.com/webmasters/APIs-Google.html)'}, 'requestId': '03326a8c-5442-4b8b-b543-1e9b0a228424', 'routeKey': '$default', 'stage': '$default', 'time': '08/Feb/2024:23:26:38 +0000', 'timeEpoch': 1707434798712}, 'body': 'eyJlbWFpbEFkZHJlc3MiOiJpcmlkaXVtZGF0YUBjcnlvc3BoZXJlaW5ub3ZhdGlvbi5jb20iLCJoaXN0b3J5SWQiOjU5MDk3Mzl9', 'isBase64Encoded': True}

        url = reverse('sbd_gmail_pub_sub-list')
        response = self.client.post(url, format='json', data=sample_pub_sub_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)