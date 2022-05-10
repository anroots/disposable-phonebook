import json
import phonenumbers
from phonenumbers import geocoder
class PhoneNumber():

    phonenumber:str
    area:str
    provider:str

    def __init__(self, phonenumber:str, provider:str) -> None:

        phonenumber_obj = phonenumbers.parse(phonenumber)
        self.phonenumber = phonenumbers.format_number(phonenumber_obj, phonenumbers.PhoneNumberFormat.E164)
        self.area = geocoder.description_for_number(phonenumber_obj, 'en')
        self.provider = provider

    def __repr__(self) -> str:
        return json.dumps({
            "number":self.phonenumber,
            "area": self.area,
            "provider":self.provider
            })

class PhoneNumberJsonEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
