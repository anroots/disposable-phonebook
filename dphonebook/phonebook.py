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
        loaded_providers = []
        for provider in number_provider_classes:
            if self.config.get('enabled_providers') and provider.domain() not in self.config.get('enabled_providers'):
                continue

            self.providers.append(provider(
                logger=self.logger,
                session=self.session_factory(),
                name=provider.domain(),
                writer=self.result_writer
            ))
            loaded_providers.append(provider.domain())
        self.logger.info(f'Loaded providers: {",".join(loaded_providers)}')

    def scrape(self):
        if not self.providers:
            self.load_providers()

        for provider in self.providers:
            provider.start()

        # Wait for all provider threads to complete
        for provider in self.providers:
            provider.join(1200)

            # Wait for max 20min, then force a stop if needed
            if provider.is_alive():
                provider.stop()
                self.logger.warning(
                    f'Thread {provider.name} timed out after 20min, only {provider.progress()}% '
                    'of results are available'
                )

        self.result_writer.write()
