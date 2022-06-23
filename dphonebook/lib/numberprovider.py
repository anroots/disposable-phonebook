import datetime
import re
from logging import Logger
from threading import Event
from threading import Thread
from typing import List
from typing import Optional

import requests

from dphonebook.lib.phonenumber import PhoneNumber
from dphonebook.lib.writer.result_writer import ResultWriter


class NumberProvider(Thread):

    # For progress % reporting
    progress_total: int = 0
    progress_current: int = 0

    # Set when thread is requested to stop scraping and exit
    _stop_event: Event

    def __init__(
        self, group=None, target=None, name=None,
        logger: Logger = None, session: requests.Session = None,
        writer: ResultWriter = None,
        args=(), kwargs=None, *, daemon=None
    ):
        self.session = session
        self.logger = logger
        self.writer = writer
        self._stop_event = Event()
        super().__init__(group=group, target=target,
                         name=name, args=args, kwargs=kwargs, daemon=daemon)

    @staticmethod
    def domain() -> str:
        pass

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def progress(self) -> float:
        if not self.progress_total or not self.progress_current:
            return 0.
        if self.progress_current > self.progress_total:
            return 100
        return round(self.progress_current * 100 / self.progress_total, 2)

    def verify_number_active(self, number: str, last_message_time: datetime.datetime = None) -> bool:
        # Number is active if last message was within one day
        if last_message_time:
            return (datetime.datetime.now() - last_message_time).days <= 1

        return False

    def last_message_time(self, number: str) -> Optional[datetime.datetime]:
        pass

    def number_to_url(self, number_uri_fragment: str) -> str:
        """Return full URL to the numbers frontend "read all messages" page

        Args:
            number_uri_fragment (str): Specific URI fragment associated with this number
        """
        return f'https://{self.domain()}{number_uri_fragment}'

    def run(self) -> List[PhoneNumber]:
        pass

    def fuzzy_time_to_datetime(self, fuzzy_time: str) -> Optional[datetime.datetime]:
        time_components = re.search(r'(\d{1,2}) (sec|second|seconds|min|minute|hour|h|day|month)s? ago', fuzzy_time)
        if not time_components:
            return None
        time_quantity = int(time_components.group(1))  # 12
        time_unit = time_components.group(2)  # minutes

        seconds_ago = time_quantity
        if time_unit in ['min', 'minute']:
            seconds_ago *= 60
        if time_unit in ['hour', 'h']:
            seconds_ago *= 3600
        if time_unit == 'day':
            seconds_ago *= 86400
        if time_unit == 'month':
            seconds_ago *= 2629800

        return datetime.datetime.now() - datetime.timedelta(seconds=seconds_ago)


class ScrapeTargetException(Exception):
    pass


class SiteNotAvailable(ScrapeTargetException):
    pass


class RateLimitReached(ScrapeTargetException):
    pass
