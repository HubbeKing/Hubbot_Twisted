from hubbot.message import TargetTypes
from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
from cobe.brain import Brain
import os


class Markov(ModuleInterface):
    help = "Markov - Yeah I'm sentient, what of it?"

    def onEnable(self):
        self.brain = Brain(os.path.join("hubbot", "data", "{}.brain".format(self.bot.server)))

    def addToBrain(self, msg):
        if "://" not in msg and len(msg) > 1:
            self.brain.learn(msg)

    def shouldTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Type in self.acceptedTypes:
            return True
        return False

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.User.Name == self.bot.nickname:
            return
        elif message.TargetType is TargetTypes.USER and not message.MessageString.startswith(self.bot.commandChar):
            reply = self.brain.reply(message.MessageString, max_len=100)
            return IRCResponse(ResponseType.Say, reply.capitalize(), message.ReplyTo)
        elif self.bot.nickname.lower() in message.MessageString.lower() and len(message.MessageList) > 1:
            messageList = [item.lower() for item in message.MessageList if item.lower() != self.bot.nickname.lower()]
            reply = self.brain.reply(" ".join(messageList), max_len=100)

            nickList = [nick.lower() for nick in self.bot.channels[message.ReplyTo].Users.keys()]
            while reply.split(" ")[0].lower() in nickList:
                reply = " ".join(reply.split(" ")[1:])
            for word in reply.split(" "):
                if word.lower() in nickList:
                    reply.replace(word, message.User.Name)
            return IRCResponse(ResponseType.Say, reply.capitalize(), message.ReplyTo)
        else:
            messageList = [item.lower() for item in message.MessageList if item.lower() != self.bot.nickname.lower()]
            self.addToBrain(" ".join(messageList))
