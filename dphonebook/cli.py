import logging
import sys
from pathlib import Path

import click
import yaml

from dphonebook.lib.writer.json_writer import JsonWriter
from dphonebook.lib.writer.stdout_writer import StdoutWriter
from dphonebook.phonebook import Phonebook


@click.group()
def main():
    pass


def logger_factory():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    streamHandler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    streamHandler.setLevel(logging.INFO)
    logger.addHandler(streamHandler)
    return logger


def load_config(config_file: str, logger: logging.Logger):

    try:
        with open(config_file, 'r') as stream:
            return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logging.error('Unable to load YAML config file %s: %s', config_file, exc)
        sys.exit(1)
    except FileNotFoundError:
        logging.error('Unable to find config file %s', config_file)
        sys.exit(1)


def writer_factory(config: dict):
    writer_type = config.get('writer', {}).get('type', 'StdoutWriter')

    # Temp, later: replace with more dynamic/intelligent loader
    if writer_type == 'StdoutWriter':
        return StdoutWriter({})
    if writer_type == 'JsonWriter':
        return JsonWriter(config['writer']['args'])
    raise Exception('Unknown writer type')


def phonebook_factory(config_file) -> Phonebook:
    logger = logger_factory()
    config = load_config(config_file, logger)
    return Phonebook(
        logger=logger,
        config=config,
        result_writer=writer_factory(config)
    )


@main.command()
@click.option('--config-file', default=Path.joinpath(Path(__file__).parent.absolute(), 'disposable-phonebook.yml'), help='Config file location')
def list(config_file: str):
    phonebook = phonebook_factory(config_file)
    phonebook.load_providers()
    for provider in phonebook.providers:
        click.echo(provider.domain())


@main.command()
@click.option('--config-file', default=Path.joinpath(Path(__file__).parent.absolute(), 'disposable-phonebook.yml'), help='Config file location')
def scrape(config_file: str):
    phonebook = phonebook_factory(config_file)
    phonebook.scrape()


if __name__ == '__main__':
    main()
