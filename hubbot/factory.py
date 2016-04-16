from twisted.internet import protocol, reactor
from hubbot.bot import Hubbot


class HubbotFactory(protocol.ReconnectingClientFactory):
    def __init__(self, server, port, channels, bothandler):
        """
        @type bothandler: hubbot.bothandler.BotHandler
        """
        self.port = port
        self.bot = Hubbot(server, channels, bothandler)
        self.protocol = self.bot
        self.initialDelay = 15.0
        self.delay = self.initialDelay
        reactor.connectTCP(server, port, self)

    def startedConnecting(self, connector):
        """
        @type connector: twisted.internet.tcp.Connector
        """
        self.bot.logger.info("-#- Started to connect to \"{}\".".format(self.transport.getPeer().host))

    def buildProtocol(self, addr):
        self.bot.logger.info("-#- Connected to \"{}\".".format(self.bot.server))
        self.bot.logger.info("-#- Resetting reconnection delay.")
        self.resetDelay()
        return self.bot

    def clientConnectionLost(self, connector, reason):
        """
        @type connector: twisted.internet.tcp.Connector
        @type reason: twisted.python.failure.Failure
        """
        if not self.bot.Quitting:
            self.bot.logger.warning("-!- Connection to \"{}\" lost, reason: \"{}\" Retrying in {} seconds.".format(self.transport.getPeer().host, reason.getErrorMessage(), self.delay))
            protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        """
        @type connector: twisted.internet.tcp.Connector
        @type reason: twisted.python.failure.Failure
        """
        self.bot.logger.warning("-!- Connection to \"{}\" failed, reason: \"{}\" Retrying in {} seconds.".format(self.transport.getPeer().host, reason.getErrorMessage(), self.delay))
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
