import datetime
import json

import phonenumbers
from phonenumbers import geocoder


class PhoneNumber():

    # The phone number in E.164 format
    phonenumber: str

    # Geographical area (country) this number belongs to
    area: str

    # ID for the provider (usually DNS name) where number was obtained from
    provider: str

    last_checked: datetime.datetime
    last_message: datetime.datetime

    # URL to the specific phone number's "view messages" page on provider site
    url: str

    def __init__(
        self,
        phonenumber: str,
        provider: str,
        last_checked: datetime.datetime = None,
        last_message: datetime.datetime = None,
        url: str = None
    ) -> None:

        phonenumber_obj = phonenumbers.parse(phonenumber)
        self.phonenumber = phonenumbers.format_number(phonenumber_obj, phonenumbers.PhoneNumberFormat.E164)
        self.area = geocoder.description_for_number(phonenumber_obj, 'en') or None
        self.provider = provider
        self.last_checked = last_checked or datetime.datetime.now()
        self.last_message = last_message
        self.url = url

    def to_dict(self) -> dict:
        return {
            'number': self.phonenumber,
            'area': self.area,
            'provider': self.provider,
            'last_message': int(self.last_message.timestamp()) if self.last_message else None,
            'last_checked': int(self.last_checked.timestamp()),
            'url': self.url
        }

    def __repr__(self) -> str:
        return json.dumps(self.to_dict())


class PhoneNumberJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, PhoneNumber):
            return o.to_dict()
        return super().default(o)
