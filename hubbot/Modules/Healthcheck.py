from twisted.protocols import basic
from twisted.internet import protocol, reactor

from hubbot.moduleinterface import ModuleInterface


class HealthcheckProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        response_body = "All is well. Ish.".encode("UTF-8")
        self.sendLine("HTTP/1.0 200 OK".encode("UTF-8"))
        self.sendLine("Content-Type: text/plain".encode("UTF-8"))
        self.sendLine(f"Content-Length: {len(response_body)}\n".encode("UTF-8"))
        self.transport.write(response_body)
        self.transport.loseConnection()


class Healthcheck(ModuleInterface):
    port = 9999

    def __init__(self, bot):
        self.healthcheck_server = protocol.ServerFactory()
        self.healthcheck_server.protocol = HealthcheckProtocol

        super().__init__(bot)

    def on_load(self):
        reactor.listenTCP(self.port, self.healthcheck_server)

    def on_unload(self):
        reactor.stopListening(self.port)

    def help(self, message):
        return f"Hosts an HTTP healthcheck server on port {self.port}."
