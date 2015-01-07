import logging
import os
import sys

from twisted.internet import reactor

from hubbot.factory import HubbotFactory
from hubbot.channel import IRCChannel
from hubbot.config import Config, ConfigError


class BotHandler:
    botfactories = {}

    def __init__(self, parsedArgs):
        self.config = Config(parsedArgs.config)
        try:
            self.config.readConfig()
        except ConfigError:
            logging.exception("An error occured when trying to read config file \"{}\".".format(parsedArgs.config))
        server = self.config["server"]
        port = self.config.itemWithDefault("port", 6667)
        channels = self.config.itemWithDefault("channels", [])
        self.startBotFactory(server, port, channels)
        reactor.run()

    def startBotFactory(self, server, port, channels):
        if server in self.botfactories:
            logging.warning("Bot for server \"{}\" was requested but one is already running!".format(server))
            return False
        else:
            logging.info("New bot for server \"{}\" requested, starting...".format(server))
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
                # this most likely means the bot in question has yet to establish a connection for whatever reason
                # TODO should probably figure out and specify what kind of exception this is
                logging.exception("Bot for server \"{}\" could not quit properly!".format(server))
                self.botfactories[server].stopTrying()
            self.unregisterFactory(server)
            logging.info("Successfully shut down bot for server \"{}\"".format(server))

    def unregisterFactory(self, server):
        if server in self.botfactories:
            del self.botfactories[server]

        if len(self.botfactories) == 0:
            logging.info("No more bots are running, stopping reactor.")
            reactor.callLater(2.0, reactor.stop)

    def shutdown(self, quitmessage="Shutting down..."):
        logging.info("Shutdown command received, shutting down EVERYTHING.")
        for server in self.botfactories.keys():
            self.stopBotFactory(server, quitmessage.encode("utf-8"))

    def restart(self, quitmessage="Restarting..."):
        logging.info("Restart command received, going down for restart.")
        reactor.addSystemEventTrigger("after", "shutdown", lambda: os.execl(sys.executable, sys.executable, *sys.argv))
        self.shutdown(quitmessage.encode("utf-8"))
