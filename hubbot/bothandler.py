import logging
import os
import sys

from twisted.internet import reactor

from hubbot.factory import HubbotFactory
from hubbot.channel import IRCChannel
from hubbot.config import Config


class BotHandler:
    botfactories = {}

    def __init__(self, parsedArgs):
        self.config = Config(parsedArgs.config)
        try:
            self.config.readConfig()
        except Exception:
            logging.exception("An error occured when trying to read config file \"{}\".".format(parsedArgs.config))
        for server in self.config["servers"]:
            port = self.config.serverItemWithDefault(server, "port", 6667)
            channels = self.config.serverItemWithDefault(server, "channels", [])
            self.startBotFactory(server, port, channels)
        reactor.run()

    def startBotFactory(self, server, port, channels):
        if server in self.botfactories:
            logging.warning("Bot for server \"{}\" was requested but one is already running!".format(server))
            return False
        if type(channels) == list:
            chanObjects = {}
            for channel in channels:
                chanObjects[channel] = IRCChannel(channel)
            botfactory = HubbotFactory(server, port, chanObjects, self)
        else:
            botfactory = HubbotFactory(server, port, channels, self)
        self.botfactories[server] = botfactory
        return True

    def stopBotFactory(self, server, quitmessage=None):
        if quitmessage is None:
            quitmessage = "ohok".encode("utf-8")
        else:
            quitmessage = quitmessage
        if server not in self.botfactories:
            logging.warning("Bot for \"{}\" does not exist yet was asked to stop.".format(server))
        else:
            logging.info("Shutting down bot for server \"{}\"".format(server))
            self.botfactories[server].bot.Quitting = True
            try:
                self.botfactories[server].bot.quit(quitmessage)
                for (name, module) in self.botfactories[server].bot.moduleHandler.modules.items():
                    module.onUnload()
            except:
                self.botfactories[server].stopTrying()
            self.unregisterFactory(server)
            logging.info("Successfully shut down bot for server \"{}\"".format(server))

    def unregisterFactory(self, server):
        if server in self.botfactories:
            del self.botfactories[server]

            if len(self.botfactories) == 0:
                logging.info("No more running bots, shutting down.")
                reactor.callLater(5.0, reactor.stop)

    def shutdown(self, quitmessage="Shutting down..."):
        quitmessage = quitmessage.encode("utf-8")
        for server in self.botfactories.keys():
            self.stopBotFactory(server, quitmessage)
        reactor.callLater(2.0, reactor.stop)

    def restart(self, quitmessage="Restarting..."):
        reactor.addSystemEventTrigger("after", "shutdown", lambda: os.execl(sys.executable, sys.executable, *sys.argv))
        quitmessage = quitmessage.encode("utf-8")
        for server in self.botfactories.keys():
            self.stopBotFactory(server, quitmessage)
        reactor.callLater(2.0, reactor.stop)
