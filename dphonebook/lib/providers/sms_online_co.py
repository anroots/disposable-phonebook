import datetime
from typing import List
from typing import Optional

from bs4 import BeautifulSoup

from dphonebook.lib.numberprovider import NumberProvider
from dphonebook.lib.numberprovider import SiteNotAvailable
from dphonebook.lib.phonenumber import PhoneNumber


class SmsOnlineCo(NumberProvider):

    @staticmethod
    def domain() -> str:
        return 'sms-online.co'

    def run(self) -> List[PhoneNumber]:

        response = self.session.get(f'https://{self.domain()}/receive-free-sms/')

        if not response.ok:
            raise SiteNotAvailable(response.content)

        page = BeautifulSoup(response.content, features='html.parser')
        number_rows = page.find_all('div', class_='number-boxes-item')

        self.progress_total = len(number_rows) - 1

        for number_row in number_rows:
            self.progress_current += 1

            if self.stopped():
                return

            number = number_row.find('h4').contents[0]
            number_link = number_row.find('a').attrs['href']
            last_message_time = self.last_message_time(number_link)

            self.writer.append(PhoneNumber(
                number,
                provider=self.domain(),
                last_message=last_message_time,
                url=number_link
            ))

    def last_message_time(self, number: str) -> Optional[datetime.datetime]:
        """Get time when last message was sent to this number
        """

        response = self.session.get(number)

        if not response.ok:
            return None

        page = BeautifulSoup(response.content, features='html.parser')
        last_message = page.find('span', class_='list-item-meta').find('span').contents[0]
        if not last_message:
            return None

        return self.fuzzy_time_to_datetime(last_message)
