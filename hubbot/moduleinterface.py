from __future__ import unicode_literals
from enum import Enum


class ModuleAccessLevel(Enum):
    ANYONE = 0
    ADMINS = 1


class ModuleInterface(object):
    triggers = []
    accepted_types = ["PRIVMSG"]
    help = "No help defined yet."
    access_level = ModuleAccessLevel.ANYONE
    priority = 0

    def __init__(self, bot):
        """
        @type bot: hubbot.bot.Hubbot
        """
        self.bot = bot

    def on_load(self):
        """
        Called when the module is loaded by the ModuleHandler
        """
        pass

    def on_unload(self):
        """
        Called when the module is unloaded by the ModuleHandler
        """
        pass

    def should_trigger(self, message):
        """
        Called by the ModuleHandler for each incoming message, to see if said message causes this module to trigger
        Default behavior is to trigger on any message that matches the accepted types and contains a matching command trigger

        @type message: hubbot.message.IRCMessage
        """
        if message.type not in self.accepted_types:
            return False
        if message.command not in self.triggers:
            return False
        return True

    def on_trigger(self, message):
        """
        Called by the ModuleHandler when shouldTrigger(message) is True.
        Contains all actions the module is to perform on the message object.

        @type message: hubbot.message.IRCMessage
        @return: hubbot.response.IRCResponse | None
        """
        pass
