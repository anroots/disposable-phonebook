from dphonebook.lib.phonenumber import PhoneNumber


class ResultWriter:

    results:list[PhoneNumber] = []

    def __init__(self, args: dict) -> None:
        self.args = args
        
    def append(self, numbers:list[PhoneNumber]):
        self.results += numbers


    def write(self):
        pass
