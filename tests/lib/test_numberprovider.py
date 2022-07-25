import unittest
from datetime import datetime
from datetime import timedelta

from dphonebook.lib.numberprovider import NumberProvider


class NumberProviderTest(unittest.TestCase):

    def test_fuzzy_time_converts_input_correctly(self):
        numberprovider = NumberProvider()
        now = datetime.now()

        expected_conversions = [
            ('25 minutes ago', now - timedelta(minutes=25)),
            ('1 hour ago', now - timedelta(hours=1)),
            ('an hour ago', now - timedelta(hours=1)),
            ('one minute ago', now - timedelta(minutes=1)),
            ('1hours ago', now - timedelta(hours=1))
        ]

        for conversion in expected_conversions:
            converted_time = numberprovider.fuzzy_time_to_datetime(conversion[0])
            self.assertIsNotNone(converted_time)
            self.assertEqual(
                int(converted_time.timestamp()),
                int(conversion[1].timestamp())
            )
