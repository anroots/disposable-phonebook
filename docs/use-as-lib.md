# Usage as a library

You can use Disposable Phonebook as a Python library in your own code.

``` python title="my_scraper.py"
import logging
from dphonebook.phonebook import Phonebook
from dphonebook.lib.writer.result_writer import ResultWriter


class MyCustomWriter(ResultWriter):
    """
    Implement a custom ResultWriter class to handle results
    """

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


```bash
$ pip3 install git+https://github.com/anroots/disposable-phonebook.git
$ python3 my_scraper.py
{"number": "+37255585858", "area": "Estonia", "provider": "dummy.example.com", "last_message": 1652610267, "last_checked": 1652610267}
{"number": "+37255000000", "area": "Estonia", "provider": "dummy.example.com", "last_message": 1652610267, "last_checked": 1652610267}
```
