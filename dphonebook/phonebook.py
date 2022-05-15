import threading
from logging import Logger

import requests

from dphonebook.lib.numberprovider import NumberProvider
from dphonebook.lib.providers import number_provider_classes
from dphonebook.lib.writer.result_writer import ResultWriter


class Phonebook:

    providers: list[NumberProvider] = []

    def __init__(self, logger: Logger, config: dict, result_writer: ResultWriter) -> None:
        self.logger = logger
        self.result_writer = result_writer
        self.config = config

    def session_factory(self) -> requests.Session:
        session = requests.Session()

        # TODO: dynamic
        session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15'})

        return session

    def load_providers(self):
        for provider in number_provider_classes:
            if self.config.get('enabled_providers') and provider.domain() not in self.config.get('enabled_providers'):
                continue

            self.providers.append(provider(
                logger=self.logger,
                session=self.session_factory()
            ))

    def scrape(self):
        if not self.providers:
            self.load_providers()

        threads = []
        for provider in self.providers:

            thread = threading.Thread(target=provider.scrape, args=[self.result_writer.append])
            thread.start()
            threads.append(thread)

        # Wait for all provider threads to complete
        for thread in threads:
            thread.join()

        self.result_writer.write()
