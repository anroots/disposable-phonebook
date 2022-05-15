# Usage from CLI

Disposable Phonebook comes with a CLI utility that can be used ad-hoc, or integrated
with other tooling such as `cron`.

```bash
$ dphonebook --help
Usage: dphonebook [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  list
  scrape

$ dphonebook scrape --help
Usage: dphonebook scrape [OPTIONS]

Options:
  --config-file TEXT  Config file location
  --help              Show this message and exit.
```

The `scrape` subcommand fetches numbers from all enabled Providers. The `--config-file` option
specifies a Yaml config file to use. Default reference config file is provided
under `dphonebook/disposable-phonebook.yml`.
