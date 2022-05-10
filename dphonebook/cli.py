import click

import logging
import sys

from dphonebook.dphonebook import DPhonebook
from dphonebook.lib.stdout_writer import StdoutWriter


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

@main.command()
def scrape():
    logger = logger_factory()

    dphonebook = DPhonebook(
        logger=logger,
        result_writer=StdoutWriter()
        )
    dphonebook.scrape()

if __name__ == '__main__':
    main()
