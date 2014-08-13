from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

"""
status.HTTP_100_CONTINUE                         status.HTTP_409_CONFLICT
status.HTTP_101_SWITCHING_PROTOCOLS              status.HTTP_410_GONE
status.HTTP_200_OK                               status.HTTP_411_LENGTH_REQUIRED
status.HTTP_201_CREATED                          status.HTTP_412_PRECONDITION_FAILED
status.HTTP_202_ACCEPTED                         status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
status.HTTP_203_NON_AUTHORITATIVE_INFORMATION    status.HTTP_414_REQUEST_URI_TOO_LONG
status.HTTP_204_NO_CONTENT                       status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
status.HTTP_205_RESET_CONTENT                    status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
status.HTTP_206_PARTIAL_CONTENT                  status.HTTP_417_EXPECTATION_FAILED
status.HTTP_300_MULTIPLE_CHOICES                 status.HTTP_428_PRECONDITION_REQUIRED
status.HTTP_301_MOVED_PERMANENTLY                status.HTTP_429_TOO_MANY_REQUESTS
status.HTTP_302_FOUND                            status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
status.HTTP_303_SEE_OTHER                        status.HTTP_500_INTERNAL_SERVER_ERROR
status.HTTP_304_NOT_MODIFIED                     status.HTTP_501_NOT_IMPLEMENTED
status.HTTP_305_USE_PROXY                        status.HTTP_502_BAD_GATEWAY
status.HTTP_306_RESERVED                         status.HTTP_503_SERVICE_UNAVAILABLE
status.HTTP_307_TEMPORARY_REDIRECT               status.HTTP_504_GATEWAY_TIMEOUT
status.HTTP_400_BAD_REQUEST                      status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED
status.HTTP_401_UNAUTHORIZED                     status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED
status.HTTP_402_PAYMENT_REQUIRED                 status.is_client_error
status.HTTP_403_FORBIDDEN                        status.is_informational
status.HTTP_404_NOT_FOUND                        status.is_redirect
status.HTTP_405_METHOD_NOT_ALLOWED               status.is_server_error
status.HTTP_406_NOT_ACCEPTABLE                   status.is_success
status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED    status.unicode_literals
status.HTTP_408_REQUEST_TIMEOUT                  
"""

MULTIPOLY = """MULTIPOLYGON (((-401141.5244410000159405 273728.5500730000203475, -587036.3772299999836832 68183.1278420000016922, -489196.9810249999864027 -39441.7579719999994268, -117407.2754459999996470 87752.4768060000060359, -401141.5244410000159405 273728.5500730000203475)))"""

class WebAPISurveyTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="user1")

    def test_site_unauth(self):
        """ site view not visible to unauthenticated user """
        url = '/api/site.json'
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_site_auth(self):
        """ site view visible to authenticated user """
        self.client.login(username="user1", password="user1")
        url = '/api/site.json'
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_view_site(self):
        """ site view visible to authenticated user """
        self.client.login(username="user1", password="user1")
        url = '/api/site'
        res = self.client.post(url, {
            'name': 'GravelSite1',
            'notes': '',
            'geometry': MULTIPOLY,
            #'user': 1,
            }, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        url = '/api/site/{:d}.json'.format(res.data['id'])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['type'], 'Feature')
        
        url = '/api/site.json'
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # import ipdb; ipdb.set_trace()
        self.assertEqual(res.data['type'], 'FeatureCollection')
        self.assertEqual(len(res.data['features']), 1)

