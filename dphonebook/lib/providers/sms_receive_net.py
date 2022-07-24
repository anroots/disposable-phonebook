import re
from typing import List

from bs4 import BeautifulSoup

from dphonebook.lib.numberprovider import NumberProvider
from dphonebook.lib.numberprovider import SiteNotAvailable
from dphonebook.lib.phonenumber import PhoneNumber


class SmsReceiveNet(NumberProvider):

    @staticmethod
    def domain() -> str:
        return 'sms-receive.net'

    def run(self) -> List[PhoneNumber]:
        response = self.session.get(f'https://{self.domain()}/')

        if not response.ok:
            raise SiteNotAvailable(response.content)

        page = BeautifulSoup(response.content, features='html.parser')
        number_rows = page.find_all('div', class_='uk-panel-box-primary')

        self.progress_total = len(number_rows) - 1

        for number_row in number_rows:
            self.progress_current += 1

            if self.stopped():
                return

            number_link = number_row.find('a').attrs['href']
            number = '+' + number_link.split('-')[0]

            number_url = self.number_to_url(f'/{number_link}')
            response = self.session.get(number_url)

            # Response HTML from the site not really stable, invalid HTML
            # that breaks proper bs4 parsing, regex seems more reliable
            fuzzy_time = re.search(r'data-label="Time.*>(.*)<\/td>', response.text).group(1)
            if not fuzzy_time:
                self.logger.warn('Unable to get SmSReceiveNet last message time for %s', number_url)
                continue

            last_message_time = self.fuzzy_time_to_datetime(fuzzy_time)

            if not self.verify_number_active(number, last_message_time):
                self.logger.info('SmsReceiveNet number %s is not active, skipping', number)
                continue

            self.writer.append(PhoneNumber(
                number,
                provider=self.domain(),
                last_message=last_message_time,
                url=number_url
            ))
