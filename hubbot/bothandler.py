import os
import sys

from twisted.internet import reactor

from bot import HubbotFactory
from channel import IRCChannel
from config import Config


class BotHandler:
    botfactories = {}

    def __init__(self, parsedArgs):
        self.parsedArgs = parsedArgs
        self.config = Config(self.parsedArgs.config)
        self.config.readConfig()
        for server in self.config["servers"]:
            port = self.config.serverItemWithDefault(server, "port", 6667)
            channels = self.config.serverItemWithDefault(server, "channels", [])
            self.startBotFactory(server, port, channels)
        reactor.run()

    def startBotFactory(self, server, port, channels):
        if server in self.botfactories:
            print "Already on server '{}'.".format(server)
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
            self.quitmessage = "ohok".encode("utf-8")
        else:
            self.quitmessage = quitmessage
        if server not in self.botfactories:
            print "ERROR: Bot for '{}' does not exist yet was asked to stop.".format(server)
        else:
            print "Shutting down bot for server '{}'".format(server)
            self.botfactories[server].protocol.Quitting = True
            try:
                self.botfactories[server].protocol.quit(quitmessage)
                for (name, module) in self.botfactories[server].protocol.moduleHandler.modules.items():
                    module.onUnload()
            except:
                self.botfactories[server].stopTrying()
            self.unregisterFactory(server)
            print "Successfully shut down bot for server '{}'".format(server)

    def unregisterFactory(self, server):
        if server in self.botfactories:
            del self.botfactories[server]

            if len(self.botfactories) == 0:
                print "No more running bots, shutting down."
                reactor.callLater(2.0, reactor.stop)

    def shutdown(self, quitmessage="Shutting down..."):
        quitmessage = quitmessage.encode("utf-8")
        for server, botfactory in self.botfactories.iteritems():
            botfactory.protocol.Quitting = True
            botfactory.protocol.quit(quitmessage)
            for (name, module) in botfactory.protocol.moduleHandler.modules.items():
                module.onUnload()
        self.botfactories = {}
        reactor.callLater(4.0, reactor.stop)

    def restart(self, quitmessage="Restarting..."):
        self.quitmessage = quitmessage.encode("utf-8")
        for server, botfactory in self.botfactories.iteritems():
            botfactory.protocol.Quitting = True
            botfactory.protocol.quit(quitmessage)
            for (name, module) in botfactory.protocol.moduleHandler.modules.items():
                module.onUnload()
        self.botfactories = {}
        reactor.callLater(2.0, self.replaceInstance)

    def replaceInstance(self):
        reactor.stop()
        python = sys.executable
        os.execl(python, python, "bothandler.py")
