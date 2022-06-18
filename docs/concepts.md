# Concepts

## Providers

A `Provider` is an online service who makes temporary phone numbers available for use.
In Disposable Phonebook, Providers are represented by dedicated classes under `dphonebook.lib.providers`.

A provider class needs to inherit from `dphonebook.lib.numberprovider.NumberProvider`, and implement
the `scrape` method.

## Writers

Writers are result-saving mechanism - where to put collected numbers? Writers are represented
by classes under `dphonebook.lib.writer`.

- `StdoutWriter` -> print output to stdout console
- `JsonWriter` -> write output as JSON into a file. This output file can be fed into other tooling as data input.
- `WebhookWriter` -> POST results (in batches) to a HTTP endpoint
