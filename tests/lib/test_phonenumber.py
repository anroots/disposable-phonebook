import json
import unittest

from dphonebook.lib.phonenumber import PhoneNumber


class PhoneNumberTest(unittest.TestCase):

    def setUp(self):
        self.phonenumber = '+37255555555'
        self.provider = 'unitest.example.com'
        self.number = PhoneNumber(self.phonenumber, self.provider)

    def test_repr_is_json_string(self):
        self.assertEqual(json.loads(str(self.number))['number'], self.phonenumber)

    def test_area_is_none_if_can_not_determine(self):
        number = PhoneNumber('+6123456789', self.provider)
        self.assertIsNone(number.area)
