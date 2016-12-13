from __future__ import unicode_literals
from hubbot.message import TargetTypes
from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
from cobe.brain import Brain
import os


class Markov(ModuleInterface):
    help = "Markov - Yeah I'm sentient, what of it?"
    accepted_types = ["PRIVMSG", "ACTION"]

    def __init__(self, bot):
        self.brain = None
        super(Markov, self).__init__(bot)

    def on_load(self):
        if self.bot.network is not None:
            self.brain = Brain(os.path.join("hubbot", "data", "{}.brain".format(self.bot.network)))
        else:
            self.brain = Brain(os.path.join("hubbot", "data", "{}.brain".format(self.bot.address)))

    def add_to_brain(self, msg):
        if "://" not in msg and len(msg) > 1:
            self.brain.learn(msg)

    def should_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.type in self.accepted_types:
            return True
        return False

    def _index_containing_substring(self, stringlist, substring):
        """
        Given a list of strings, returns the index of the first element that contains a given substring
        If none exists, returns -1
        """
        for i, s in enumerate(stringlist):
            if substring in s:
                return i
        return -1

    def _clean_up_string(self, string):
        new_string = "".join(c for c in string if ord(c) >= 0x20).lstrip("~").lstrip("!").lstrip(".").lstrip("@")
        return new_string.replace("(.+.+)", "")

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.user.name == self.bot.nickname:
            return
        elif message.target_type is TargetTypes.USER and message.command not in self.bot.module_handler.mapped_triggers:
            reply = ""
            while len(reply.split()) < 2:
                reply = self.brain.reply(message.message_string, max_len=100)
                reply = self._clean_up_string(reply)
            return IRCResponse(ResponseType.SAY, reply.capitalize(), message.reply_to)
        elif self.bot.nickname.lower() in message.message_string.lower() and len(message.message_list) > 1:
            reply = ""
            while len(reply.split()) < 2:
                message_list = [item for item in message.message_list if item.lower() != self.bot.nickname.lower()]
                reply = self.brain.reply(" ".join(message_list), max_len=100)
                nick_list = [nick.lower() for nick in self.bot.channels[message.reply_to].users.keys()]
                for nick in nick_list:
                    if nick in reply.lower():
                        reply_list = reply.lower().split()
                        nick_index = self._index_containing_substring(reply_list, nick)
                        new_list = [item for item in reply_list if nick not in item]
                        new_list.insert(nick_index, message.user.name)
                        reply = " ".join(new_list)
                reply = self._clean_up_string(reply)
            return IRCResponse(ResponseType.SAY, reply.capitalize(), message.reply_to)
        elif message.type == "PRIVMSG":
            message_list = [item.lower() for item in message.message_list if item.lower() != self.bot.nickname.lower()]
            self.add_to_brain(" ".join(message_list))
