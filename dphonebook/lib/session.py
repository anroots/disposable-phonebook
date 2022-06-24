import gzip
import json
import os
import random

import requests


class Session:

    user_agents: list = []

    def __init__(self) -> None:
        self.load_user_agents()

    def make(self) -> requests.Session:
        session = requests.Session()

        session.headers.update(
            {'User-Agent': random.choice(self.user_agents)})

        return session

    def user_agents_file(self) -> str:
        dir_path = os.path.dirname(os.path.abspath(__file__))
        agents_file = os.path.join(dir_path, '..', 'vendor', 'user-agents', 'user-agents.json.gz')
        return os.path.abspath(agents_file)

    def load_user_agents(self):
        decompressedFile = gzip.open(self.user_agents_file(), mode='rb')
        user_agents = json.loads(decompressedFile.read())
        del decompressedFile

        for user_agent in user_agents:
            self.user_agents.append(user_agent['userAgent'])
