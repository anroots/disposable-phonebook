import datetime
from typing import List
from typing import Optional

from bs4 import BeautifulSoup

from dphonebook.lib.numberprovider import NumberProvider
from dphonebook.lib.numberprovider import SiteNotAvailable
from dphonebook.lib.phonenumber import PhoneNumber


class ReceiveSmsFreeCc(NumberProvider):

    @staticmethod
    def domain() -> str:
        return 'receive-sms-free.cc'

    def country_links(self, page_number=1) -> list:
        """Recursive function to get all the "country XX phone numbers" subcategory pages

        Args:
            page_number (int, optional): Current pagination number. Defaults to 1.

        Returns:
            list: URLs for country-based subpages
        """
        response = self.session.get(self.number_to_url(f'/regions/{page_number}.html'))

        # We've reached the last page, abort recursion
        if response.status_code == 404 or page_number > 20:
            return []

        if not response.ok:
            raise SiteNotAvailable(response.content)

        page = BeautifulSoup(response.content, features='html.parser')

        links = []
        for link in page.find_all('a', class_='link_btn'):
            links.append(link.attrs['href'])

        return links + self.country_links(page_number=page_number + 1)

    def country_number_links(self, country_link, page_number=1) -> list:
        response = self.session.get(f'{country_link}/{page_number}.html')

        if not response.ok:
            raise SiteNotAvailable(response.content)

        page = BeautifulSoup(response.content, features='html.parser')

        links = []
        for number_box in page.find('div', class_='index-case').find_all('li', class_='wow'):
            links.append(number_box.find('a').attrs['href'])

        # We've reached the last page (site does not return 404 status code)
        if not links or page_number > 120:
            return []

        return links + self.country_number_links(country_link, page_number=page_number + 1)

    def run(self) -> List[PhoneNumber]:

        number_links = []

        country_links = self.country_links()
        for country_link in country_links:
            number_links += self.country_number_links(country_link)

        self.progress_total = len(number_links) - 1
        self.logger.info(
            'Found %d numbers from %s, starting validation...',
            len(number_links),
            self.domain()
        )

        for number_link in number_links:
            self.progress_current += 1

            if self.stopped():
                return

            # https://receive-sms-free.cc/Free-USA-Phone-Number/17078776869/
            last_message_time = self.last_message_time(number_link)

            number = f'+{number_link.split("/")[-2]}'
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
        """Get time when last message was sent to this number
        """

        response = self.session.get(number)

        if not response.ok:
            return None

        page = BeautifulSoup(response.content, features='html.parser')
        messages_table = page.find('div', class_='casetext')
        first_message_row = messages_table.find_all('div', class_='row')[1]
        last_message_time = first_message_row.find('div', class_='col-xs-0').contents[0]

        return self.fuzzy_time_to_datetime(last_message_time)
