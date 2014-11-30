

class ModuleInterface(object):
    triggers = []
    acceptedTypes = ['PRIVMSG']
    help = '<no help defined (yet)>'
    accessLevel = 0
    # 0 = Anyone
    # 1 = Admins only

    def __init__(self, bot):
        """
        @type bot: Hubbot.Hubbot
        """
        self.bot = bot

    def onLoad(self):
        pass

    def onUnload(self):
        pass

    def shouldTrigger(self, message):
        """
        @type message: IRCMessage.IRCMessage
        """
        if message.Type not in self.acceptedTypes:
            return False
        if message.Command not in self.triggers:
            return False

        return True

    def onTrigger(self, message):
        """
        @type message: IRCMessage.IRCMessage
        """
        pass