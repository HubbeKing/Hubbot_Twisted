from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
from collections import defaultdict
import os
import random


class Markov(ModuleInterface):
    markov = defaultdict(list)
    STOP_WORD = "\n"
    chattiness = 0.05
    chainLength = 2
    maxWords = 100
    help = "Markov - Yeah I'm sentient, what of it?"

    def addToBrain(self, msg, write=True):
        if "://" in msg:
            return
        if write:
            with open(os.path.join("hubbot", "data", "{}.brain".format(self.bot.server)), "a") as brainFile:
                brainFile.write(msg + "\n")
        buf = [self.STOP_WORD] * self.chainLength
        for word in msg.split():
            self.markov[tuple(buf)].append(word)
            del buf[0]
            buf.append(word)
        self.markov[tuple(buf)].append(self.STOP_WORD)

    def generateSentence(self, msg):
        buf = msg.split()[:self.chainLength]
        if len(msg.split()) > self.chainLength:
            message = buf[:]
        else:
            message = []
            for i in xrange(self.chainLength):
                message.append(random.choice(self.markov[random.choice(self.markov.keys())]))
        for i in xrange(self.maxWords):
            try:
                nextWord = random.choice(self.markov[tuple(buf)])
            except IndexError:
                continue
            if nextWord == self.STOP_WORD:
                break
            message.append(nextWord)
            del buf[0]
            buf.append(nextWord)
        return " ".join(message)

    def onLoad(self):
        if os.path.exists(os.path.join("hubbot", "data", "{}.brain".format(self.bot.server))):
            with open(os.path.join("hubbot", "data", "{}.brain".format(self.bot.server)), "r") as brainFile:
                for line in brainFile:
                    self.addToBrain(line, write=False)

    def shouldTrigger(self, message):
        return True

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if not message.User:
            return
        if message.MessageList[0].startswith(self.bot.nickname):
            msg = " ".join(message.MessageList[1:])
            self.addToBrain(msg)
            if random.random() <= self.chattiness:
                sentence = self.generateSentence(msg)
                if sentence:
                    return IRCResponse(ResponseType.Say, sentence, message.ReplyTo)
        else:
            msg = " ".join(message.MessageList)
            self.addToBrain(msg)
