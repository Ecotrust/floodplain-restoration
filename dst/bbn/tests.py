from django.test import TestCase
from os.path import abspath, join, dirname
import os
from bbn import BeliefNetwork
import random

# Example from http://www.bnlearn.com/bnrepository/
# Copyright 2013 Marco Scutari. 
# The contents of this page are licensed under the Creative 
# Commons Attribution-Share Alike License. 
# ( http://creativecommons.org/licenses/by-sa/3.0/ )


class BBNUnitTests(TestCase):

    def setUp(self):
        self.bif = abspath(join(dirname(__file__), "test_data", "cancer.bif"))
        self.outbif = '/tmp/test%s.bif' % random.random()

    def tearDown(self):
        try:
            os.remove(self.outbif)
        except:
            pass

    def test_from_bif(self):
        bn = BeliefNetwork.from_bif(self.bif)
        self.assertEquals(
            sorted(list(bn.variables.keys())), 
            ['Cancer', 'Dyspnoea', 'Pollution', 'Smoker', 'Xray'])
        self.assertEquals(
            sorted(list(bn.probabilities.keys())), 
            ['Cancer', 'Dyspnoea', 'Pollution', 'Smoker', 'Xray'])

    def test_to_bif(self):
        bn = BeliefNetwork.from_bif(self.bif)
        bn.to_bif(self.outbif)

        bn2 = BeliefNetwork.from_bif(self.outbif)
        self.assertEquals(bn2, bn)

