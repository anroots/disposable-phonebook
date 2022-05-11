import datetime
from typing import List

from bs4 import BeautifulSoup

from dphonebook.lib.numberprovider import NumberProvider
from dphonebook.lib.numberprovider import SiteNotAvailable
from dphonebook.lib.phonenumber import PhoneNumber


class ReceiveSmsCo(NumberProvider):

    def domain(self):
        return 'www.receivesms.co'

    def scrape(self) -> List[PhoneNumber]:

        response = self.session.get(f'https://{self.domain()}/active-numbers/')

        if not response.ok:
            raise SiteNotAvailable(response.content)

        page = BeautifulSoup(response.content, features='html.parser')
        links = page.find_all('a')

        for link in links:
            if not link.has_attr('data-clipboard-text'):
                continue
            number = link.contents.pop()
            last_message_time = self.last_message_time(number)
            if not self.verify_number_active(number, last_message_time):
                self.logger.info(
                    '%s number %s is not active, skipping', self.domain(), number)
                continue
            yield PhoneNumber(
                number,
                provider=self.domain(),
                last_message=self.last_message_time(number)
            )

    def last_message_time(self, number: str) -> datetime.datetime:
        return None
