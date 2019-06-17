import signal

from twisted.internet import reactor

from hubbot.moduleinterface import ModuleInterface


class SignalHandler(ModuleInterface):
    def on_load(self):
        signal.signal(signal.SIGTERM, self._signal_received)

    def _signal_received(self, signal_number):
        if signal_number == signal.SIGTERM:
            # likely docker stopping our container, disconnect and stop cleanly
            self.bot.quit("Shutting down...")
            reactor.callLater(2.0, reactor.stop)
