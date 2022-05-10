from typing import List
from dphonebook.lib.numberprovider import NumberProvider, SiteNotAvailable
from dphonebook.lib.phonenumber import PhoneNumber
from bs4 import BeautifulSoup

class ReceiveSmss(NumberProvider):

    def scrape(self) -> List[PhoneNumber]:

        response = self.session.get('https://receive-smss.com/')

        if not response.ok:
            raise SiteNotAvailable(response.content)

        page = BeautifulSoup(response.content, features='html.parser')
        number_links = page.find_all("h4", class_="number-boxes-itemm-number")

        for number_element in number_links:
            number = number_element.contents.pop()
            if not self.verify_number_active(number):
                self.logger.info('ReceiveSmss number %s is not active, skipping', number)
                continue
            yield PhoneNumber(
                number,
                provider=self.__class__.__name__,
            )

    def verify_number_active(self, number:str) -> bool:
        response = self.session.get(f'https://receive-smss.com/sms/{number.strip("+")}/')
        if not response.ok:
            return False

        page = BeautifulSoup(response.content, features='html.parser')

        # Get the first row on "received messages" table (the latest message)
        try:
            latest_message = page.find('table', class_='wrptable').find('tbody').find('tr')

            # Fuzzy time ("43 minutes ago") on the 2nd column
            latest_time = latest_message.find_all('td')[1].find('span').contents.pop()

            # Assuming less than a day from latest activity on this number
            # Provider increments fuzzy time units from hours -> days -> ...
            # Unclear how "true" reported message times are
            time_units = ['second ago', 'seconds ago', 'minute ago', 'minutes ago', 'hour ago', 'hours ago']
            for time_unit in time_units:
                if time_unit in latest_time:
                    return True
        except Exception as e:
            self.logger.warn(e)
            return False

        return False
