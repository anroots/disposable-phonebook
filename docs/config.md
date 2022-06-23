disposable-phonebook can be configured through a config file
when used through CLI. You can specify a custom config file with a CLI option.

See `dphonebook/disposable-phonebook.yml` for defaults and available options.

Minimum viable config file looks like this:

```yaml
writer:
  type: StdoutWriter
enabled_providers:
  - dummy.example.com
```
