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

    def _indexContainingSubstring(self, list, substring):
        for i, s in enumerate(list):
            if substring in s:
                return i
        return -1

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.User.Name == self.bot.nickname:
            return
        elif message.MessageList[1].lower() in self.bot.moduleHandler.mappedTriggers:
            return
        elif message.TargetType is TargetTypes.USER and not message.MessageString.startswith(self.bot.commandChar):
            reply = self.brain.reply(message.MessageString, max_len=100)
            return IRCResponse(ResponseType.Say, reply.lstrip("!").capitalize(), message.ReplyTo)
        elif self.bot.nickname.lower() in message.MessageString.lower() and len(message.MessageList) > 1:
            messageList = [item for item in message.MessageList if item.lower() != self.bot.nickname.lower()]
            reply = self.brain.reply(" ".join(messageList), max_len=100)

            nickList = [nick.lower() for nick in self.bot.channels[message.ReplyTo].Users.keys()]
            for nick in nickList:
                if nick in reply.lower():
                    replyList = reply.lower().split()
                    nickIndex = self._indexContainingSubstring(replyList, nick)
                    newList = [item for item in replyList if nick not in item]
                    newList.insert(nickIndex, message.User.Name)
                    reply = " ".join(newList)
            return IRCResponse(ResponseType.Say, reply.lstrip("!").capitalize(), message.ReplyTo)
        else:
            messageList = [item.lower() for item in message.MessageList if item.lower() != self.bot.nickname.lower()]
            self.addToBrain(" ".join(messageList))
