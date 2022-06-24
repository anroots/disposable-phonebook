# disposable-phonebook

Collect "disposable" phone numbers from various internet sites that offer
"receive free SMS to an anonymous number" functionality.

```bash
$ dphonebook scrape
[{"number": "+16462879071", "area": "New York", "provider": "receive-smss.com", "last_message": 1652437175, "last_checked": 1652438795},
{"number": "+16466623058", "area": "New York", "provider": "receive-smss.com", "last_message": 1652437776, "last_checked": 1652438796}]
```

This is useful to online service providers, who want to restrict usage of such numbers
on customer profiles, for security reasons (avoiding publicly available 2FA codes).

## Quickstart

```bash
$ pip3 install disposable-phonebook
$ dphonebook scrape
```

See [docs](https://anroots.github.io/disposable-phonebook/) for further details.

## Online API

This project powers [disposable-phonebook.com](https://disposable-phonebook.com), where
a list of disposable numbers is available over a free HTTP API.

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

### Releasing

Releases are uploaded automaticaly to pypi on new Git tag creation.

- Make sure [Changelog.md](Changelog.md) is updated
- Update version number in [setup.py](setup.py)
- `git tag 0.2.0`

## Contribution

Want to add or fix something? Send a pull request.

This project uses (with thanks):

- [python-phonenumbers](https://github.com/daviddrysdale/python-phonenumbers) for phone number
  formatting and metadata
- [top-user-agents](https://github.com/Kikobeats/top-user-agents) for UA list

## License

Apache2 license (see: [LICENSE](LICENSE))
