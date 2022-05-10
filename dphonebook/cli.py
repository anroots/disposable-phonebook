import importlib
import click

import logging
import sys

import yaml
from dphonebook.lib.writer import *
from dphonebook.dphonebook import DPhonebook


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

def load_config(config_file:str, logger:logging.Logger):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error('Unable to load YAML config file %s: %s', config_file, exc)
            raise exc

def writer_factory(config:dict):
    writer_type = config.get('writer', {}).get('type', 'StdoutWriter')

    # Temp, later: replace with more dynamic/intelligent loader
    if writer_type == 'StdoutWriter':
        return StdoutWriter(config['writer']['args'])
    if writer_type == 'JsonWriter':
        return JsonWriter(config['writer']['args'])
    raise Exception('Unknown writer type')
    
@main.command()
@click.option('--config-file', default='disposable-phonebook.yml', help='Config file location')
def scrape(config_file:str):
    logger = logger_factory()
    config = load_config(config_file, logger)
    dphonebook = DPhonebook(
        logger=logger,
        config=config,
        result_writer=writer_factory(config)
        )
    dphonebook.scrape()

if __name__ == '__main__':
    main()
