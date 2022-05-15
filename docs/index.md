# Disposable Phonebook

Scraper for collecting "disposable phone numbers" - phone numbers that are made available for anonymous users to receive SMS to.

## Quickstart

``` bash
git clone git@github.com:anroots/disposable-phonebook.git
cd disposable-phonebook
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pip install --editable .
dphonebook --help
dphonebook scan
cat scraped-numbers.json
```
