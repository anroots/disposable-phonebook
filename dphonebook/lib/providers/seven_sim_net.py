import datetime
from typing import List
from typing import Optional

from bs4 import BeautifulSoup

from dphonebook.lib.numberprovider import NumberProvider
from dphonebook.lib.numberprovider import SiteNotAvailable
from dphonebook.lib.phonenumber import PhoneNumber


class SevenSimNet(NumberProvider):

    @staticmethod
    def domain() -> str:
        return '7sim.net'

    def run(self) -> List[PhoneNumber]:

        response = self.session.get(f'https://{self.domain()}/')

        if not response.ok:
            raise SiteNotAvailable(response.content)

        page = BeautifulSoup(response.content, features='html.parser')
        number_links = page.find_all('a', class_='npn')

        self.progress_total = len(number_links) - 1

        for number_element in number_links:
            self.progress_current += 1

            if self.stopped():
                return

            number_link = number_element.attrs['href']
            number = number_element.contents[0]

            last_message_time = self.last_message_time(number_link)

            if not self.verify_number_active(number, last_message_time):
                self.logger.info('%s number %s is not active, skipping', self.domain(), number)
                continue

            self.writer.append(PhoneNumber(
                number,
                provider=self.domain(),
                last_message=last_message_time,
                url=number_link
            ))

    def last_message_time(self, number: str) -> Optional[datetime.datetime]:
        response = self.session.get(number)
        page = BeautifulSoup(response.content, features='html.parser')

        messages_table = page.find('table', class_='num-sms')
        fuzzy_time = messages_table.find('tbody').find('td', class_='t-m-r')

        # No messages for this phone number (yet)?
        if not fuzzy_time:
            return None

        return self.fuzzy_time_to_datetime(fuzzy_time.contents[0])
