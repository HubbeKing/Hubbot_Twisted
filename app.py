from __future__ import unicode_literals
from hubbot.config import Config, ConfigError
from hubbot.factory import HubbotFactory
import argparse
import logging
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A derpy Twisted IRC bot.")
    parser.add_argument("-c", "--config", help="The configuration file to user", type=str, default="hubbot.yaml")
    parser.add_argument("-l", "--logfile", help="The file used for global error logging", type=str, default="hubbot.log")
    options = parser.parse_args()

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    streamHandler = logging.StreamHandler(stream=sys.stdout)
    streamHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%H:%M:%S'))
    streamHandler.setLevel(logging.INFO)
    root_logger.addHandler(streamHandler)
    # set up file for error logging
    fileHandler = logging.FileHandler(filename=options.logfile)
    fileHandler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y/%m/%d-%H:%M:%S'))
    fileHandler.setLevel(logging.ERROR)
    root_logger.addHandler(fileHandler)

    config = Config(options.config)
    try:
        config.read_config()
    except ConfigError:
        root_logger.exception("Failed to load config {!r}".format(options.config))
    else:
        factory = HubbotFactory(config)
