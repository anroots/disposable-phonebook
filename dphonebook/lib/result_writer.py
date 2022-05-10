from dphonebook.lib.phonenumber import PhoneNumber


class ResultWriter:

    results:list[PhoneNumber] = []


    def append(self, numbers:list[PhoneNumber]):
        self.results += numbers


    def write(self):
        pass
