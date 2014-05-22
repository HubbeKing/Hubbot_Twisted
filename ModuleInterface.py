

class ModuleInterface(object):
    triggers = []
    acceptedTypes = ['PRIVMSG']
    help = '<no help defined (yet)>'

    def __init__(self, bot):
        self.bot = bot
        self.onLoad()

    def onLoad(self):
        pass

    def onUnload(self):
        pass

    def hasAlias(self, message):
        if message.Command in self.bot.moduleHandler.commandAliases.keys():
            return True
        else:
            return False

    def shouldTrigger(self, message):
        if message.Type not in self.acceptedTypes:
            return False
        if message.Command not in self.triggers:
            return False

        return True

    def onTrigger(self, message):
        pass