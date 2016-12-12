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
        pass

    def on_unload(self):
        pass

    def should_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.type not in self.accepted_types:
            return False
        if message.command not in self.triggers:
            return False
        return True

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        pass
