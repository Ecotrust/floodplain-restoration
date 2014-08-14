from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from survey.models import Question
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
POLY = """POLYGON ((-401141.5244410000159405 273728.5500730000203475, -587036.3772299999836832 68183.1278420000016922, -489196.9810249999864027 -39441.7579719999994268, -117407.2754459999996470 87752.4768060000060359, -401141.5244410000159405 273728.5500730000203475))"""
SITE1 = {
    'name': 'GravelSite1',
    'notes': 'Notes on Site 1',
    'geometry': MULTIPOLY,
}
USER1 = dict(username="user1", password="user1")
USER2 = dict(username="user2", password="user2")


class WebAPIIntegrationTests(APITestCase):
    """ These are not `unit` tests; they test the public HTTP interface
    and simulate actual workflows on the client side. Minimal use of the 
    python API will be employed, ensuring that these tests remain as
    the canonical (testable) example of API usage """

    fixtures = ['questions']

    def setUp(self):
        self.user1 = User.objects.create_user(**USER1)
        self.user2 = User.objects.create_user(**USER2)

    def test_site_unauth(self):
        """ site view not visible to unauthenticated user """
        url = '/api/site.json'
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_site_auth(self):
        """ site view visible to authenticated user """
        self.client.login(**USER1)
        url = '/api/site.json'
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_view_site(self):
        """ create a set and get it's geojson back """
        self.client.login(**USER1)
        res = self.client.post('/api/site', SITE1, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        url = '/api/site/{:d}.json'.format(res.data['id'])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['type'], 'Feature')

        url = '/api/site.json'
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['type'], 'FeatureCollection')
        self.assertEqual(len(res.data['features']), 1)

    def test_site_private(self):
        """ site1 is not visible to anyone but user """
        self.client.login(**USER1)
        res = self.client.post('/api/site', SITE1, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        url = '/api/site/{:d}.json'.format(res.data['id'])
        self.client.logout()

        self.client.login(**USER2)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_site_suitability(self):
        """ query belief network of the site """
        self.client.login(**USER1)
        res = self.client.post('/api/site', SITE1, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        site_id = res.data['id']

        url = '/api/site/{:d}/suitability'.format(site_id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        baseline = res.data['suitability']

        question_id = Question.objects.get(name='infrastructure_constraints').pk

        # post an input node
        url = '/api/node'
        data = {
            'name': 'na',
            'notes': 'Notes about this answer',
            'site': site_id,
            'question': question_id,
            'value': 0.0 
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Query suitability again and ensure it changed
        url = '/api/site/{:d}/suitability.json'.format(site_id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        newsuitability = res.data['suitability']
        self.assertNotEqual(baseline, newsuitability)

    def test_site_status(self):
        """ Complete workflow to completed site status """
        self.client.login(**USER1)
        res = self.client.post('/api/site', SITE1, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        site_id = res.data['id']

        url = '/api/site/{:d}/status.json'.format(site_id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        baseline = res.data['complete']
        self.assertEqual(baseline, False)

        missing_questions = res.data['missing_questions']
        import random
        for question_id in missing_questions:
            # loop through missing quesitons and post an input node
            url = '/api/node'
            data = {
                'name': 'na',
                'notes': 'Notes about this answer',
                'site': site_id,
                'question': question_id,
                'value': random.random()
            }
            res = self.client.post(url, data)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Query status again and ensure missing questions is None
        url = '/api/site/{:d}/status'.format(site_id)
        res = self.client.get(url)
        step2 = res.data['complete']
        missing_questions = res.data['missing_questions']
        self.assertEqual(step2, False)  # still need pits
        self.assertEqual(len(missing_questions), 0)

        # Need to add a pit
        url = '/api/pit'
        data = {
            'name': 'testpit',
            'site': site_id,
            'geometry': POLY
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Query status again and ensure complete
        url = '/api/site/{:d}/status'.format(site_id)
        res = self.client.get(url)
        step2 = res.data['complete']
        self.assertEqual(step2, True)

class SurveyUnitTests(TestCase):
    fixtures = ['questions']

    def test_systemcheck(self):
        from survey.validate import systemcheck, SystemCheckError
        # should not raise anything
        systemcheck()

        Question.objects.get(name='infrastructure_constraints').delete()
        self.assertRaises(SystemCheckError, systemcheck)

