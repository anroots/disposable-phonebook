from typing import List
from dphonebook.lib.numberprovider import NumberProvider
from dphonebook.lib.phonenumber import PhoneNumber


class ReceiveSmss(NumberProvider):

    def scrape(self) -> List[PhoneNumber]:

        return [PhoneNumber("555"), PhoneNumber("666")]
