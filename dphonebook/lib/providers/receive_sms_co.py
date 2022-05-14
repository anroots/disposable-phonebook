import datetime
import re
from typing import List
from typing import Optional

from bs4 import BeautifulSoup
from bs4 import PageElement

from dphonebook.lib.numberprovider import NumberProvider
from dphonebook.lib.numberprovider import SiteNotAvailable
from dphonebook.lib.phonenumber import PhoneNumber


class ReceiveSmsCo(NumberProvider):

    @staticmethod
    def domain() -> str:
        return 'www.receivesms.co'

    def is_number_row(self, row: PageElement) -> bool:
        return bool(self.number_from_row(row))

    def number_from_row(self, row: PageElement) -> str:
        """
        Extract phone number from a table <tr> row
        <td><a class="btn" data-clipboard-text="+19159969739">+19159969739</a></td>
        """
        for link in row.find_all('a'):
            if link.has_attr('data-clipboard-text'):
                return link.attrs['data-clipboard-text']
        return ''

    def number_link_from_row(self, row: PageElement) -> str:
        """
        Extract phone number link from a table <tr> row
        <td><a href="/us-phone-number/3491/" target="_self">Read received SMS</a></td>
        """
        for link in row.find_all('a'):
            if not link.contents.pop() == 'Read received SMS':
                continue
            return link.attrs['href']

    def scrape(self, callback: callable) -> List[PhoneNumber]:

        response = self.session.get(f'https://{self.domain()}/active-numbers/')

        if not response.ok:
            raise SiteNotAvailable(response.content)

        page = BeautifulSoup(response.content, features='html.parser')
        number_rows = page.find('table', class_='table-hover').find_all('tr')

        for number_row in number_rows:

            # Skip header row in table
            if not self.is_number_row(number_row):
                continue

            number = self.number_from_row(number_row)
            number_link = self.number_link_from_row(number_row)

            last_message_time = self.last_message_time(number, number_link)
            if not self.verify_number_active(number, last_message_time):
                self.logger.info(
                    '%s number %s is not active, skipping', self.domain(), number)
                continue
            callback(PhoneNumber(
                number,
                provider=self.domain(),
                last_message=last_message_time
            ))

    def last_message_time(self, number: str, link: str = None) -> Optional[datetime.datetime]:
        """Get time when last message was sent to this number

        Args:
            number (str): Phone number
            link (str, optional): URI fragment (/us/phone-number/3491/) to phone number details. Defaults to None.
        """
        response = self.session.get(f'https://{self.domain()}{link}')

        if not response.ok:
            raise SiteNotAvailable(response.content)

        page = BeautifulSoup(response.content, features='html.parser')

        message_row = page.find('div', id='msgtbl').find_all('div', class_='row')[1]
        timestamp_cell = message_row.find_all('div', class_='mobile_hide')[1]

        return self.fuzzy_time_to_datetime(timestamp_cell.contents.pop())

    def fuzzy_time_to_datetime(self, fuzzy_time: str) -> Optional[datetime.datetime]:
        time_components = re.search(r'(\d{1,2}) (sec|seconds|min|minute|hour|day|month)s? ago', fuzzy_time)
        if not time_components:
            return None
        time_quantity = int(time_components.group(1))  # 12
        time_unit = time_components.group(2)  # minutes

        seconds_ago = time_quantity
        if time_unit in ['min', 'minute']:
            seconds_ago *= 60
        if time_unit == 'hour':
            seconds_ago *= 3600
        if time_unit == 'day':
            seconds_ago *= 86400
        if time_unit == 'month':
            seconds_ago *= 2629800

        return datetime.datetime.now() - datetime.timedelta(seconds=seconds_ago)
