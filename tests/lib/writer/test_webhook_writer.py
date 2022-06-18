import logging
import queue
import unittest
from unittest import mock

from dphonebook.lib.phonenumber import PhoneNumber
from dphonebook.lib.writer.webhook_writer import RequestSender


class RequestSenderTest(unittest.TestCase):
    @mock.patch('dphonebook.lib.writer.webhook_writer.Session.post')
    def setUp(self, mock_session):
        self.phonenumber = '+37255555555'
        self.number = PhoneNumber(self.phonenumber, 'unitest.example.com')

        self.work_queue = queue.Queue()
        self.request_sender = RequestSender(
            self.work_queue,
            mock_session,
            'localhost',
            logging.getLogger()
        )
        self.mock_session = mock_session

    def test_threaded_runner_exits_when_queue_empty(self):

        self.work_queue.put([self.number])
        self.request_sender.start()
        self.assertTrue(self.request_sender.is_alive())
        self.work_queue.put(None)
        self.work_queue.join()

        self.assertFalse(self.request_sender.is_alive())

    def test_sent_post_request_contains_expected_body(self):
        self.work_queue.put([self.number, self.number])
        self.request_sender.start()
        self.work_queue.put(None)
        self.work_queue.join()

        number_json = str(self.number)
        self.mock_session.post.assert_called_with(
            'localhost',
            data='{"numbers": [' + number_json + ', ' + number_json + ']}'
        )
