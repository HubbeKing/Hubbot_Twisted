from twisted.internet import reactor, protocol

from hubbot.moduleinterface import ModuleInterface


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def dataReceived(self, data):
        """As soon as any data is received, write it back."""
        self.transport.write(data)


class Healthcheck(ModuleInterface):
    port = 9999

    def __init__(self, bot):
        self.healthcheck_server = protocol.ServerFactory()
        self.healthcheck_server.protocol = Echo

        super().__init__(bot)

    def on_load(self):
        reactor.listenTCP(self.port, self.healthcheck_server)

    def on_unload(self):
        reactor.stopListening(self.port)

    def help(self, message):
        return f"Hosts an HTTP healthcheck server on port {self.port}."
