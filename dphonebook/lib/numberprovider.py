from logging import Logger
from typing import List
from dphonebook.lib.phonenumber import PhoneNumber


class NumberProvider:
    def __init__(self, logger:Logger) -> None:
        self.logger = logger

    def is_online(self):
        pass

    def scrape(self) -> List[PhoneNumber]:
        pass
