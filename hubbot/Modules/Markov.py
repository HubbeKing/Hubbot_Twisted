from __future__ import unicode_literals
from twisted.internet import reactor
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
        self.brain_file = ""
        super(Markov, self).__init__(bot)

    def on_load(self):
        if self.bot.network is not None:
            self.brain = Brain(os.path.join("hubbot", "data", "brains", "{}.brain".format(self.bot.network)))
            self.brain_file = self.bot.network
            self.bot.logger.info("Markov module loaded successfully.")
        else:
            self.bot.logger.info("Markov module could not get network name, delaying load...")
            self.bot.module_handler.unload_module("Markov")
            reactor.callLater(5.0, self.bot.module_handler.load_module, "Markov")

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

    @staticmethod
    def _index_containing_substring(string_list, substring):
        """
        Given a list of strings, returns the index of the first element that contains a given substring
        If none exists, returns -1
        """
        for i, s in enumerate(string_list):
            if substring in s:
                return i
        return -1

    @staticmethod
    def _clean_up_string(string):
        new_string = "".join(c for c in string if ord(c) >= 0x20).lstrip("~").lstrip("!").lstrip(".").lstrip("@")
        return new_string.replace("(.+.+)", "")

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.command == "markov" and message.user.name in self.bot.admins:
            if len(message.parameter_list) == 2 and message.parameter_list[0].lower() == "load":
                self.brain = None
                self.brain = Brain(os.path.join("hubbot", "data", "brains", "{}.brain".format(message.parameter_list[1])))
                self.brain_file = message.parameter_list[1]
                return IRCResponse(ResponseType.SAY, "Successfully loaded markov brain {}".format(self.brain_file), message.reply_to)
            elif len(message.parameter_list) == 2 and message.parameter_list[0].lower() == "unload":
                self.brain = None
                old_name = self.brain_file
                self.brain_file = ""
                return IRCResponse(ResponseType.SAY, "Successfully unloaded markov brain {}".format(old_name), message.reply_to)
            else:
                available_brains = [brain.split(".", 1)[0] for brain in os.listdir(os.path.join("hubbot", "data", "brains")) if brain.split(".", 1)[1] == "brain"]
                return IRCResponse(ResponseType.SAY, "Current loaded brain is {}".format(self.brain_file), message.reply_to), \
                       IRCResponse(ResponseType.SAY, "Available brains are: {}".format(", ".join(available_brains)), message.reply_to)
        elif message.command == "markov":
            return IRCResponse(ResponseType.SAY, "Current loaded brain is {}".format(self.brain_file), message.reply_to)
        elif message.user.name == self.bot.nickname:
            return
        elif message.target_type is TargetTypes.USER and message.command not in self.bot.module_handler.mapped_triggers:
            if self.brain is None:
                return
            reply = ""
            while len(reply.split()) < 2:
                reply = self.brain.reply(message.message_string, max_len=100)
                reply = self._clean_up_string(reply)
            return IRCResponse(ResponseType.SAY, reply.capitalize(), message.reply_to)
        elif self.bot.nickname.lower() in message.message_string.lower() and len(message.message_list) > 1:
            if self.brain is None:
                return
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
            if self.brain_file == self.bot.network:
                message_list = [item.lower() for item in message.message_list if item.lower() != self.bot.nickname.lower()]
                self.add_to_brain(" ".join(message_list))
