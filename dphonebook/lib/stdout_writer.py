from logging import Logger
from dphonebook.lib.result_writer import ResultWriter


class StdoutWriter(ResultWriter):

    def write(self):
        for number in self.results:
            print(number)
