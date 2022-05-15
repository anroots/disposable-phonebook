import datetime
from typing import List
from typing import Optional

from dphonebook.lib.numberprovider import NumberProvider
from dphonebook.lib.phonenumber import PhoneNumber


class DummyExampleCom(NumberProvider):
    """
    Sample provider that returns dummy values
    """
    @staticmethod
    def domain() -> str:
        return 'dummy.example.com'

    def scrape(self, callback: callable) -> List[PhoneNumber]:
        example_numbers = ['+37255585858', '+37255000000']
        for number in example_numbers:
            last_message_time = self.last_message_time(number)

            callback(PhoneNumber(
                number,
                provider=self.domain(),
                last_message=last_message_time
            ))

    def last_message_time(self, number: str) -> Optional[datetime.datetime]:
        """Get time when last message was sent to this number

        Args:
            number (str): Phone number
        """

        return datetime.datetime.now()
