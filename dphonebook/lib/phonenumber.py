import json


class PhoneNumber():
    def __init__(self, phonenumber:str) -> None:
        self.phonenumber = phonenumber

    def __repr__(self) -> str:
        return json.dumps({"number":self.phonenumber})

class PhoneNumberJsonEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
