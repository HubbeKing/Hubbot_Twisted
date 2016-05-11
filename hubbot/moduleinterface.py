from enum import Enum


class ModuleAccessLevel(Enum):
    ANYONE = 0
    ADMINS = 1


class ModuleInterface(object):
    triggers = []
    acceptedTypes = ['PRIVMSG']
    help = '<no help defined (yet)>'
    runInThread = False
    timeout = 5
    accessLevel = ModuleAccessLevel.ANYONE

    priority = 0

    def __init__(self, bot):
        """
        @type bot: hubbot.bot.Hubbot
        """
        self.bot = bot

    def onEnable(self):
        pass

    def onDisable(self):
        pass

    def shouldTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Type not in self.acceptedTypes:
            return False
        if message.Command not in self.triggers:
            return False

        return True

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        pass
