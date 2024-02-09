from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from data.mongodb import delete_mongodb_collection

from instruments.models import Deployment, Instrument
from authentication.models import APIKey
from real_time_data.models import *
from instruments.models import Deployment, Instrument


class TestSBDPubSubPostRequest(APITestCase):
    
    """    
    Test for initiating decoding when a POST request is made from the Gmail inbox. 

    RUN THESE TESTS WITH:
    python3 manage.py test real_time_data.tests.test_sbd_pub_sub_post_request --keepdb
    """

    def setUp(self):
        self.instrument = Instrument.objects.create(
            name='Test instrument')
        
        self.deployment = Deployment.objects.create(
            name='Test deployment', instrument=self.instrument)
        self.real_time_data_object = RealTimeData.objects.create(iridium_imei='300434066254600', deployment=self.deployment)

    def test_sbd_pub_sub_post_request(self):

        sample_pub_sub_payload = {'emailAddress': 'iridiumdata@cryosphereinnovation.com', 'historyId': '5930967'}

        url = reverse('sbd_gmail_pub_sub-list')
        response = self.client.post(url, format='json', data=sample_pub_sub_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        sbd_data_object = SBDData.objects.get(deployment=self.deployment)
        self.assertEqual(sbd_data_object.sbd_filename, '300434066150890_000819.sbd')
        self.assertEqual(len(sbd_data_object.sbd_binary.tobytes()), 275)