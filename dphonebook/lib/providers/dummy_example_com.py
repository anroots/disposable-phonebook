import datetime
import time
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

    def run(self) -> List[PhoneNumber]:
        example_numbers = ['+37255585858', '+37255000000']

        self.progress_total = len(example_numbers) - 1

        for number in example_numbers:
            self.progress_current += 1

            if self.stopped():
                return

            last_message_time = self.last_message_time(number)

            self.writer.append(PhoneNumber(
                number,
                provider=self.domain(),
                last_message=last_message_time,
                url='http://localhost'
            ))

            # Simulate network lag for example purposes
            time.sleep(2)

    def last_message_time(self, number: str) -> Optional[datetime.datetime]:
        """Get time when last message was sent to this number

        Args:
            number (str): Phone number
        """

        return datetime.datetime.now()
