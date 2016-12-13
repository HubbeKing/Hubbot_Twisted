from __future__ import unicode_literals
import datetime
import os
import sys
from twisted.internet import reactor
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel


class BotHandling(ModuleInterface):
    triggers = ["quit", "quitfrom", "restart", "shutdown"]
    access_level = ModuleAccessLevel.ADMINS

    def help(self, message):
        help_dict = {
            "bothandling": "restart, shutdown - Restart, and Shutdown. Fairly self-explanatory.",
            "restart": "restart - Restarts the entire bot.",
            "shutdown": "shutdown - Shuts the entire bot down."
        }
        return help_dict[message.parameter_list[0].lower()]

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.command == "restart":
            if datetime.datetime.utcnow() > self.bot.start_time + datetime.timedelta(seconds=10):
                self.bot.quitting = True
                reactor.addSystemEventTrigger("after", "shutdown", lambda: os.execl(sys.executable, sys.executable, *sys.argv))
                self.bot.quit("Restarting...".encode("utf-8"))
                reactor.callLater(2.0, reactor.stop)
                return

        elif message.command == "shutdown":
            if datetime.datetime.utcnow() > self.bot.start_time + datetime.timedelta(seconds=10):
                self.bot.quitting = True
                self.bot.quit("Shutting down...".encode("utf-8"))
                reactor.callLater(2.0, reactor.stop)
                return
