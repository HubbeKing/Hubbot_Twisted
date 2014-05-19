import GlobalVars


class ModuleInterface(object):
    triggers = []
    acceptedTypes = ['PRIVMSG']
    help = '<no help defined (yet)>'

    def __init__(self):
        self.onStart()

    def onStart(self):
        pass

    def aliased(self, message):
        if message.Type in self.acceptedTypes and message.Command in GlobalVars.commandAliases.keys():
            return True

    def shouldTrigger(self, message):
        if message.Type not in self.acceptedTypes:
            return False
        if message.Command not in self.triggers:
            return False

        return True

    def onTrigger(self, Hubbot, message):
        pass