from hubbot.config import Config, ConfigError
from hubbot.factory import HubbotFactory
import argparse
import logging
import sys


def exception_handler(type, value, tb):
    logging.getLogger().exception("Uncaught exception: {!r}".format(value))

if __name__ == "__main__":
    logger = logging.getLogger("startup")
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    parser = argparse.ArgumentParser(description="A derpy Twisted IRC bot.")
    parser.add_argument("-c", "--config", help="The configuration file to user", type=str, default="hubbot.yaml")
    parser.add_argument("-l", "--logfile", help="The file used for global error logging", type=str, default="hubbot.log")
    options = parser.parse_args()

    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)
    streamHandler = logging.StreamHandler(stream=sys.stdout)
    streamHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%H:%M:%S'))
    streamHandler.setLevel(logging.INFO)
    rootLogger.addHandler(streamHandler)
    # set up file for error logging
    fileHandler = logging.FileHandler(filename=options.logfile)
    fileHandler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y/%m/%d-%H:%M:%S'))
    fileHandler.setLevel(logging.ERROR)
    rootLogger.addHandler(fileHandler)
    sys.excepthook = exception_handler

    config = Config(options.config)
    try:
        config.read_config()
    except ConfigError:
        logger.exception("Failed to load config {!r}".format(options.config))
    else:
        factory = HubbotFactory(config)
