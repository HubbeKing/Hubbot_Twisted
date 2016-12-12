from twisted.internet import protocol, reactor
from hubbot.bot import Hubbot
import logging


class HubbotFactory(protocol.ReconnectingClientFactory):
    def __init__(self, config):
        """
        @type config: hubbot.config.Config
        """
        self.logger = logging.getLogger("factory")

        self.port = config.item_with_default("port", 6667)
        self.address = config["address"]
        self.bot = Hubbot(self, config)
        self.protocol = self.bot
        reactor.connectTCP(self.address, self.port, self)
        reactor.run()

    def startedConnecting(self, connector):
        self.logger.info(" - Started connecting to {!r}".format(connector.host))

    def buildProtocol(self, addr):
        self.logger.info(" - Connected to {!r}".format(self.address))
        self.logger.info(" - Resetting connection delay")
        self.resetDelay()
        return self.bot

    def clientConnectionFailed(self, connector, reason):
        self.logger.warning("-!- Connection to {!r} failed, reason: {!r}".format(connector.host, reason.getErrorMessage()))
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        if not self.bot.quitting:
            self.logger.warning("-!- Connection to {!r} lost, reason {!r}".format(connector.host, reason.getErrorMessage()))
            protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
