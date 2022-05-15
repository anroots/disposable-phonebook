# Usage as a library

You can use Disposable Phonebook as a Python library in your own code.

```bash
$ pip3 install git+https://github.com/anroots/disposable-phonebook.git
```

``` python
import logging
from dphonebook.phonebook import Phonebook
from dphonebook.lib.writer.result_writer import ResultWriter


class MyCustomWriter(ResultWriter):

    def write(self):
        """
        This method will be called by dphonebook.Phonebook once scraping has concluded.
        self.results will hold scraped PhoneNumber objects
        """
        for number in self.results:
            print(number)
            # do_something_meaningful_with_number(number)

# Provide configuration options for the Phonebook instance
# See main config file reference for available options
config = {
  'enabled_providers': ['dummy.example.com']
}

phonebook = Phonebook(
  logger=logging.getLogger(),
  config=config,
  result_writer=MyCustomWriter()
)

phonebook.scrape()
```
