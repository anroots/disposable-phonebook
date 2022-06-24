from logging import Logger

from dphonebook.lib.numberprovider import NumberProvider
from dphonebook.lib.providers import number_provider_classes
from dphonebook.lib.session import Session
from dphonebook.lib.writer.result_writer import ResultWriter


class Phonebook:

    providers: list[NumberProvider] = []

    def __init__(self, logger: Logger, config: dict, result_writer: ResultWriter) -> None:
        self.logger = logger
        self.result_writer = result_writer
        self.config = config

    def load_providers(self):
        loaded_providers = []
        for provider in number_provider_classes:
            if self.config.get('enabled_providers') and provider.domain() not in self.config.get('enabled_providers'):
                continue

            session = Session()
            self.providers.append(provider(
                logger=self.logger,
                session=session.make(),
                name=provider.domain(),
                writer=self.result_writer
            ))
            loaded_providers.append(provider.domain())

        if not loaded_providers:
            raise RuntimeError('No providers loaded, please check the config file')

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
