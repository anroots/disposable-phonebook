import logging

from dphonebook.lib.phonenumber import PhoneNumber


class ResultWriter:

    results: list[PhoneNumber] = []

    def __init__(self, args: dict = None, logger: logging.Logger = None) -> None:
        self.args = args

    def append(self, number: PhoneNumber):
        self.results.append(number)

    def write(self):
        pass
