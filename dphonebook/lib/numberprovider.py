from logging import Logger
from typing import List
from dphonebook.lib.phonenumber import PhoneNumber
import requests

class NumberProvider:
    def __init__(self, logger:Logger, session:requests.Session) -> None:
        self.logger = logger
        self.session = session

    def verify_number_active(self, number:str) -> bool:
        pass

    def scrape(self) -> List[PhoneNumber]:
        pass

class SiteNotAvailable(Exception):
    pass

