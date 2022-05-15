# Disposable Phonebook

Disposable Phonebook is a scraper for collecting "disposable phone numbers" -
phone numbers that are made available for anonymous users online, for free, for receiving SMS to.

_Project status: pre-alpha, in development. Not suited for production use._

## Quickstart

``` bash
$ pip3 install disposable-phonebook
$ dphonebook --help
$ dphonebook scan
$ cat scraped-numbers.json
```

## What problem does this project solve?

There are various service providers who allow customers to register for an account.
For different reasons (ex: [KYC](https://en.wikipedia.org/wiki/Know_your_customer) requirements
or SMS 2FA security), it might be desirable to dissallow the use of throwaway anonymous phone numbers
on user profile.

This project aims to develop a tool to collect such numbers, from the service providers who make
the numbers available to anonymous visitors.

!!! warning Warning
     You should consider your use-case and risks – collected numbers should be a signal, not the source of truth. Temporary number service providers might list numbers they don't actually control.

## Privacy

The phone numbers scraped are publicly listed (a public resource), and not associated with individuals.
Hence no personally identifiable information is collected.

## Source

[github.com/anroots/disposable-phonebook](https://github.com/anroots/disposable-phonebook)
