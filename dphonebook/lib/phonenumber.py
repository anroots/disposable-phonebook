import datetime
import json

import phonenumbers
from phonenumbers import geocoder


class PhoneNumber():

    phonenumber: str
    area: str
    provider: str
    last_checked: datetime.datetime
    last_message: datetime.datetime

    def __init__(self, phonenumber: str, provider: str, last_checked: datetime.datetime = None, last_message: datetime.datetime = None) -> None:

        phonenumber_obj = phonenumbers.parse(phonenumber)
        self.phonenumber = phonenumbers.format_number(phonenumber_obj, phonenumbers.PhoneNumberFormat.E164)
        self.area = geocoder.description_for_number(phonenumber_obj, 'en')
        self.provider = provider
        self.last_checked = last_checked or datetime.datetime.now()
        self.last_message = last_message

    def to_dict(self) -> dict:
        return {
            'number': self.phonenumber,
            'area': self.area,
            'provider': self.provider,
            'last_message': int(self.last_message.timestamp()) if self.last_message else None,
            'last_checked': int(self.last_checked.timestamp())
        }

    def __repr__(self) -> str:
        return json.dumps(self.to_dict())


class PhoneNumberJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, PhoneNumber):
            return o.to_dict()
            return json.dumps(o.to_dict())
        return super().default(o)
