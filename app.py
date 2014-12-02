import argparse
from hubbot.bothandler import BotHandler

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A derpy Twisted IRC bot.")
    parser.add_argument("-c", "--config", help="The configuration file to use", type=str, default="hubbot.yaml")
    options = parser.parse_args()

    bothandler = BotHandler(options)
