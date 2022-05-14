# disposable-phonebook

Collect "disposable" phone numbers from various internet sites that offer
"receive free SMS to an anonymous number" functionality.

```bash
$ dphonebook scrape
[{"number": "+16462879071", "area": "New York", "provider": "receive-smss.com", "last_message": 1652437175, "last_checked": 1652438795},
{"number": "+16466623058", "area": "New York", "provider": "receive-smss.com", "last_message": 1652437776, "last_checked": 1652438796}]
```

## Intended use

Intended use-case: for service providers who require a phone number to be associated with a user account,
and want to filter out (blocklist) fake numbers.

## PII considerations

The phone numbers scraped are publicly listed and not associated with individuals.
No PII is collected.

## Development

Requires Python 3.10

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pip install --editable .
dphonebook --help
```

- Install [Editorconfig](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig) extension
- Install [pre-commit hooks](https://pre-commit.com/#install)


## Contribution

Want to add or fix something? Send a pull request.

## License

Apache2 license (see: [LICENSE](LICENSE))
