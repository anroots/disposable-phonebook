from logging import Logger
from dphonebook.lib.numberprovider import NumberProvider
from dphonebook.lib.providers import number_provider_classes
from dphonebook.lib.writer.result_writer import ResultWriter


class DPhonebook:

    providers:list[NumberProvider]

    def __init__(self, logger: Logger, config:dict, result_writer:ResultWriter) -> None:
        self.providers = []
        self.logger = logger
        self.result_writer = result_writer
        self.config = config

    def load_providers(self):
        for provider in number_provider_classes:
            self.providers.append(provider(self.logger))

    def scrape(self, include_providers:list=[]):
        if not self.providers:
            self.load_providers()

        for provider in self.providers:
            if include_providers and type(provider).__name__ not in include_providers:
                continue
            self.result_writer.append(provider.scrape())

        self.result_writer.write()


