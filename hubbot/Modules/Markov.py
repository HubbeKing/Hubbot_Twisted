from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
from cobe.brain import Brain
import os


class Markov(ModuleInterface):
    help = "Markov - Yeah I'm sentient, what of it?"

    def onLoad(self):
        self.brain = Brain(os.path.join("hubbot", "data", "{}.brain".format(self.bot.server)))

    def onUnload(self):
        for channel in self.bot.channels:
            response = IRCResponse(ResponseType.Say, "Fine, I'll shut up.", channel.Name)
            self.bot.moduleHandler.sendResponse(response)

    def addToBrain(self, msg):
        if "://" not in msg and len(msg) > 1:
            self.brain.learn(msg)

    def shouldTrigger(self, message):
        return True

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.User is None or message.Channel is None or message.User.Name == self.bot.nickname:
            return
        if message.MessageList[0].startswith(self.bot.nickname) and len(message.MessageList) > 1:
            reply = self.brain.reply(" ".join(message.MessageList[1:]), max_len=50)
            return IRCResponse(ResponseType.Say, reply.capitalize(), message.ReplyTo)
        else:
            self.addToBrain(" ".join(message.MessageList))
