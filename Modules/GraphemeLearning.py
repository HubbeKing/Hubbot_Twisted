from ModuleInterface import ModuleInterface
from SimpleHal import SimpleHAL


class GraphemeLearning(ModuleInterface):
    help = "learns how to speak from your words."

    def onLoad(self):
        self.bot.brain = SimpleHAL()
        self.bot.brain.load("data/{}.brain".format(self.bot.server))

    def onUnload(self):
        self.bot.brain.save("data/{}.brain".format(self.bot.server))

    def shouldTrigger(self, message):
        return True

    def onTrigger(self, message):
        msgToUse = message.MessageString.replace(self.bot.nickname, "")
        msgToUse = msgToUse.replace(self.bot.nickname.lower(), "")
        if "www" not in msgToUse and "://" not in msgToUse:
            self.bot.brain._learn(msgToUse)