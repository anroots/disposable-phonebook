import datetime
import re
from typing import List
from typing import Optional

from bs4 import BeautifulSoup

from dphonebook.lib.numberprovider import NumberProvider
from dphonebook.lib.numberprovider import SiteNotAvailable
from dphonebook.lib.phonenumber import PhoneNumber


class ReceiveSmss(NumberProvider):

    @staticmethod
    def domain() -> str:
        return 'receive-smss.com'

    def scrape(self, callback: callable) -> List[PhoneNumber]:

        response = self.session.get(f'https://{self.domain()}/')

        if not response.ok:
            raise SiteNotAvailable(response.content)

        page = BeautifulSoup(response.content, features='html.parser')
        number_links = page.find_all('h4', class_='number-boxes-itemm-number')

        for number_element in number_links:
            number = number_element.contents.pop()
            last_message_time = self.last_message_time(number)
            if not self.verify_number_active(number, last_message_time):
                self.logger.info('ReceiveSmss number %s is not active, skipping', number)
                continue
            callback(PhoneNumber(
                number,
                provider=self.domain(),
                last_message=last_message_time
            ))

    def fuzzy_time_to_datetime(self, fuzzy_time: str) -> datetime.datetime:
        time_components = re.search(r'(\d{1,2}) (second|minute|hour|day)s? ago', fuzzy_time)

        time_quantity = int(time_components.group(1))  # 12
        time_unit = time_components.group(2)  # minutes

        seconds_ago = time_quantity
        if time_unit == 'minute':
            seconds_ago *= 60
        if time_unit == 'hour':
            seconds_ago *= 3600
        if time_unit == 'day':
            seconds_ago *= 86400

        return datetime.datetime.now() - datetime.timedelta(seconds=seconds_ago)

    def last_message_time(self, number: str) -> Optional[datetime.datetime]:
        response = self.session.get(f'https://{self.domain()}/sms/{number.strip("+")}/')
        if not response.ok:
            return None

        page = BeautifulSoup(response.content, features='html.parser')

        # Get the first row on "received messages" table (the latest message)
        try:
            latest_message = page.find('table', class_='wrptable').find('tbody').find('tr')

            # Fuzzy time ("43 minutes ago") on the 2nd column
            latest_time = latest_message.find_all('td')[2].find('span').contents.pop()

            # Assuming less than a day from latest activity on this number
            # Provider increments fuzzy time units from hours -> days -> ...
            # Unclear how "true" reported message times are
            return self.fuzzy_time_to_datetime(latest_time)
        except Exception as e:
            self.logger.warn(e)

        return None
