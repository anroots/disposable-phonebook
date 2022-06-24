import os
import unittest

from dphonebook.lib.session import Session


class SessionTest(unittest.TestCase):

    def setUp(self):
        self.session = Session()

    def test_user_agents_file_path_is_a_file(self):
        agents_file = self.session.user_agents_file()
        self.assertTrue(os.path.exists(agents_file))

    def test_user_agent_list_is_loaded_from_gzip(self):
        self.session.load_user_agents()
        self.assertGreater(len(self.session.user_agents), 1000)

    def test_session_make_uses_random_user_agent(self):

        session1 = self.session.make()
        session2 = self.session.make()

        self.assertNotEqual(session1.headers['User-Agent'], session2.headers['User-Agent'])
        self.assertFalse(session1 == session2)
