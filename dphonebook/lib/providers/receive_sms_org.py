import datetime
from typing import List
from typing import Optional

from bs4 import BeautifulSoup

from dphonebook.lib.numberprovider import NumberProvider
from dphonebook.lib.numberprovider import SiteNotAvailable
from dphonebook.lib.phonenumber import PhoneNumber


class ReceiveSmsOrg(NumberProvider):

    @staticmethod
    def domain() -> str:
        return 'www.receivesms.org'

    def scrape(self, callback: callable) -> List[PhoneNumber]:

        # Front page: links to country-specific sub-pages
        response = self.session.get(f'https://{self.domain()}/')

        if not response.ok:
            raise SiteNotAvailable(response.content)

        page = BeautifulSoup(response.content, features='html.parser')
        country_rows = page.find_all('tr', class_='clickable-row')

        self.progress_total = len(country_rows) - 1

        # Iterate over country rows, fetch the sub-page
        for country_row in country_rows:
            self.progress_current += 1

            country_numbers_uri = country_row.find('a').attrs['href']
            response = self.session.get(f'https://{self.domain()}{country_numbers_uri}')

            if not response.ok:
                self.logger.warning(f'Sub-page {country_numbers_uri} not available for {self.domain()}')
                continue

            page = BeautifulSoup(response.content, features='html.parser')
            number_rows = page.find_all('tr', class_='clickable-row')

            self.progress_total += len(number_rows) - 1

            # Iterate over country-specific numbers table rows
            for number_row in number_rows:
                self.progress_current += 1

                number_link_element = number_row.find_all('a')[1]
                number_link = number_link_element.attrs['href']
                number = number_link_element.contents[0]

                last_message_time = self.last_message_time(number_link)
                if not self.verify_number_active(number, last_message_time):
                    self.logger.info(f'{self.domain} number %s is not active, skipping', number)
                    continue
                callback(PhoneNumber(
                    number,
                    provider=self.domain(),
                    last_message=last_message_time,
                    url=self.number_to_url(number_link)
                ))

    def last_message_time(self, number: str) -> Optional[datetime.datetime]:
        """Get time of last received message

        Args:
            number (str): URI fragment to specific number page
        """
        response = self.session.get(self.number_to_url(number))
        if not response.ok:
            self.logger.warning(f'Sub-page {number} not available for {self.domain()}')
            return None

        page = BeautifulSoup(response.content, features='html.parser')

        # Some numbers might have 0 received SMS listed
        if not page.find('div', class_='btn-time'):
            return None
        last_message_time = page.find('div', class_='btn-time').contents[0]

        return self.fuzzy_time_to_datetime(last_message_time)
