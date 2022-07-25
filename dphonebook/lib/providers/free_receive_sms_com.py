import datetime
from typing import List
from typing import Optional

from bs4 import BeautifulSoup

from dphonebook.lib.numberprovider import NumberProvider
from dphonebook.lib.numberprovider import SiteNotAvailable
from dphonebook.lib.phonenumber import PhoneNumber


class FreeReceiveSmsCom(NumberProvider):

    @staticmethod
    def domain() -> str:
        return 'www.freereceivesms.com'

    def run(self) -> List[PhoneNumber]:

        response = self.session.get(f'https://{self.domain()}/en/')

        if not response.ok:
            raise SiteNotAvailable(response.content)

        page = BeautifulSoup(response.content, features='html.parser')
        number_elements = page.find_all('div', class_='number-boxes-item')

        self.progress_total = len(number_elements) - 1

        for number_element in number_elements:
            self.progress_current += 1

            if self.stopped():
                return

            # Site mixes ad rows with numbers, skip them
            if 'adsbygoogle' in str(number_element.contents):
                continue

            number_link = self.number_to_url(number_element.find('a').attrs['href'])
            number = number_element.find('h4').contents[0].replace(' ', '')

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

        fuzzy_time = page.find('div', class_='border-bottom')\
            .find('div', class_='d-lg-block')\
            .find('span')

        # No messages for this phone number (yet)?
        if not fuzzy_time:
            return None
        fuzzy_time = fuzzy_time.contents[0]
        return self.fuzzy_time_to_datetime(fuzzy_time)
