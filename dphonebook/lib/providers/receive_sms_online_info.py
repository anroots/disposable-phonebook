import datetime
import re
import time
from typing import List
from typing import Optional

from bs4 import BeautifulSoup

from dphonebook.lib.numberprovider import NumberProvider
from dphonebook.lib.numberprovider import RateLimitReached
from dphonebook.lib.numberprovider import SiteNotAvailable
from dphonebook.lib.phonenumber import PhoneNumber


class ReceiveSmsOnlineInfo(NumberProvider):

    # Rate limit (seconds) between numbers
    short_sleep_time: int = 15

    # Rate limit (seconds) for longer wait of breached rate-limit cooldown
    long_sleep_time: int = 60

    @staticmethod
    def domain() -> str:
        return 'receive-sms-online.info'

    def scrape(self, callback: callable) -> List[PhoneNumber]:

        response = self.session.get(f'https://{self.domain()}/')

        if not response.ok:
            raise SiteNotAvailable(response.content)

        page = BeautifulSoup(response.content, features='html.parser')
        number_cells = page.find('div', class_='Table').find_all('div', class_='Cell')

        self.progress_total = len(number_cells) - 1

        for number_cell in number_cells:
            self.progress_current += 1

            number_link = number_cell.find('a')
            number = number_link.contents[1].strip()
            number_uri = number_link.attrs['href']

            try:
                last_message_time = self.last_message_time(number, number_uri)
            except RateLimitReached:
                self.logger.warning(
                    'Breached RateLimit for %s, sleeping %d seconds and retrying (once)',
                    self.domain(),
                    self.long_sleep_time
                )
                time.sleep(self.long_sleep_time)

                try:
                    last_message_time = self.last_message_time(number, number_uri)
                except RateLimitReached:
                    self.logger.warning(
                        'Skipping number %s (unable to verify - rate limit breached), sleeping %d seconds',
                        number,
                        self.long_sleep_time
                    )
                    time.sleep(self.long_sleep_time)
                    continue

            if not self.verify_number_active(number, last_message_time):
                self.logger.info('%s number %s is not active, skipping', self.domain(), number)
                continue

            callback(PhoneNumber(
                number,
                provider=self.domain(),
                last_message=last_message_time,
                url=self.number_to_url(f'/{number_uri}')
            ))

            # Server-side rate-limit on /script_a.php, need to slow down
            self.logger.info(f'Sleeping {self.short_sleep_time} seconds between calls to {self.domain()}...')
            time.sleep(self.short_sleep_time)

    def get_ajax_url(self, number: str, number_uri: str) -> Optional[str]:
        """Get URL of the "load number messages" AJAX API endpoint
        URL is embedded in Javascript on the page and is dynamic for each page load
        """
        response = self.session.get(self.number_to_url(f'/{number_uri}'))
        if not response.ok:
            return None
        ajax = re.search(r'\/script_a.php\?key=(.+)&phone', response.text)
        ajax_key = ajax.group(1)
        time = round(datetime.datetime.now().timestamp())

        return f'https://{self.domain()}/script_a.php?key={ajax_key}&phone={number.strip("+")}&alt_x={time}'

    def last_message_time(self, number: str, number_uri: str) -> Optional[datetime.datetime]:
        ajax_url = self.get_ajax_url(number, number_uri)

        if not ajax_url:
            return None

        # XMLHttpRequest header mandatory, server fails response if not present
        response = self.session.get(ajax_url, headers={'x-requested-with': 'XMLHttpRequest'})

        # Agressive rate-limits on server side observed
        if response.status_code == 429:
            raise RateLimitReached

        if not response.ok or 'Incorrect URL address' in response.text:
            return None

        # Using regex seems to be more reliable than bs4 here, as some of the rendered
        # messages were seen crashing the bs4 parser (unable to identify cells correctly due to encoding)
        last_message_time = re.search(' datetime="(.*)" ', response.text)

        if not last_message_time:
            return None

        return datetime.datetime.strptime(last_message_time.group(1), '%Y-%m-%dT%H:%M:%SZ')
