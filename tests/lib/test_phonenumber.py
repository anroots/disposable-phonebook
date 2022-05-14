import json
import unittest

from dphonebook.lib.phonenumber import PhoneNumber


class PhoneNumberTest(unittest.TestCase):

    def setUp(self):
        self.phonenumber = '+37255555555'
        self.number = PhoneNumber(self.phonenumber, 'unitest.example.com')

    def test_repr_is_json_string(self):
        self.assertEqual(json.loads(str(self.number))['number'], self.phonenumber)
