import json

from dphonebook.lib.phonenumber import PhoneNumberJsonEncoder
from dphonebook.lib.writer.result_writer import ResultWriter


class JsonWriter(ResultWriter):
    output_file_path: str

    def __init__(self, args: dict) -> None:
        super().__init__(args)
        self.output_file_path = self.args.get('file')
        if not self.output_file_path:
            raise Exception(f'Invalid filename "{self.output_file_path}" given for JsonWriter')

    def write(self):

        with open(self.output_file_path, 'w') as outfile:
            outfile.write(json.dumps(self.results, cls=PhoneNumberJsonEncoder))
