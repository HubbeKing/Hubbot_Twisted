import argparse
import logging
import os
import sys
from hubbot.bothandler import BotHandler
from newDB import createDB

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A derpy Twisted IRC bot.")
    parser.add_argument("-c", "--config", help="The configuration file to use", type=str, default="hubbot.yaml")
    options = parser.parse_args()
    if not os.path.exists(os.path.join("hubbot", "data", "data.db")):
        createDB()
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    bothandler = BotHandler(options)
