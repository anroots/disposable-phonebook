# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.1] - 2022-06-24

### Fixed

- Include missing `tqdm` dependency on package install
- Include user-agent data files on package install

## [0.4.0] - 2022-06-24

### Added

- Add provider for `receive-sms-free.cc`
- Use random user agent per each new `requests.Session`

## [0.3.0] - 2022-06-23

### Added

- Add max timeout per scraper thread (20min) - once it's reached, the thread
  gracefully exits. This prevents one long-running or hung thread from causing
  and infinite block on whole execution. `Provider` classes need to check for
  `self.stopped() -> bool` during execution cycles.
- Add provider for `sms-online.co`

### Changed

- BREAKING: Change class spec of `NumberProvider`: it now directly inherits from
  `threading.Thread`. `def scrape(self)` was renamed to `def run(self)`, callback
  `Writer` is now provided via class constructor

## [0.2.2] - 2022-06-19

### Added

- Add "url" field to output. Points at web page for reading SMS contents
- Add `www.receivesms.org` provider

## [0.2.1] - 2022-06-18

### Added

- Add WebhookWriter for sending results as HTTP POST requests

## [0.2.0] - 2022-06-18

### Added

- Add support for ReceiveSmsOnlineInfo provider
- Add support for interactive progress bar on CLI

## [0.1.0] - 2022-05-15

Initial release
