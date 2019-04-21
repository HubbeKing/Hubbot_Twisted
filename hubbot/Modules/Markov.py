from twisted.internet import reactor
from hubbot.message import TargetTypes
from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
from cobe_hubbot.brain import Brain
import os
import re
import sqlite3
import unicodedata


class Markov(ModuleInterface):
    help = "Markov - Markov chain replies. Bot admins can use +markov load/unload to do brain surgery."
    accepted_types = ["PRIVMSG", "ACTION"]

    def __init__(self, bot):
        self.brain = None
        self.brain_file = ""
        self.banword_regexes = []
        self.banwords_regex = re.compile("(?!)")
        # should match against nothing, making sure replies are still generated if we have no banned words
        super(Markov, self).__init__(bot)

    def on_load(self):
        if self.bot.network is not None:
            self.brain = Brain(os.path.join("hubbot", "data", "brains", "{}.brain".format(self.bot.network)))
            self.brain_file = self.bot.network
            self._create_banwords_table()
            self._load_banwords_regexes()
            self.bot.logger.info("Markov module loaded successfully.")
        else:
            self.bot.logger.info("Markov module could not get network name, delaying load...")
            self.bot.module_handler.unload_module("Markov")
            reactor.callLater(5.0, self.bot.module_handler.load_module, "Markov")

    def _create_banwords_table(self):
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS markov_banwords_regexes (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, regex TEXT NOT NULL)")
            conn.commit()

    def _load_banwords_regexes(self):
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM markov_banwords_regexes"):
                self.banword_regexes.append(row[1])
        if len(self.banword_regexes) > 0:
            self.banwords_regex = re.compile("|".join(self.banword_regexes), flags=re.IGNORECASE)

    def _add_banned_word(self, banned_word):
        regex = r"\b({})\b".format(banned_word)
        self._add_banword_regex(regex)
            
    def _add_banword_regex(self, banned_regex):
        self.banword_regexes.append(banned_regex)
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO markov_banwords_regexes VALUES (NULL, ?)", (banned_regex,))
        self.banwords_regex = re.compile("|".join(self.banword_regexes), flags=re.IGNORECASE)

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

    def _generate_clean_reply(self, message_string, max_len=100, user_nick=None, replace_nicks=None):
        """
        Generate a safe/clean reply to message_string,
        regenerating if we encounter a banned word,
        and replacing any instance of any of the 'replace_nicks' with 'user_nick'
        """
        reply = ""
        if self.brain is None:
            return reply
        while len(reply.split()) < 2 or self.banwords_regex.match(reply):
            reply = self.brain.reply(message_string, max_len=max_len)
            reply = self._clean_up_string(reply)
            if replace_nicks is not None:
                for nick in replace_nicks:
                    if nick in reply.lower():
                        reply_list = reply.lower().split()
                        nick_index = self._index_containing_substring(reply_list, nick)
                        new_list = [item for item in reply_list if nick not in item]
                        new_list.insert(nick_index, user_nick)
                        reply = " ".join(new_list)
        return reply

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
        """
        Prune characters that aren't letters from string, and also try to remove malicious regexes from it
        """
        new_string = "".join(c for c in string if ord(c) >= 0x20)
        while unicodedata.category(new_string[0]) not in ["Ll", "Lu"]:
            new_string = new_string[1:]
        return new_string.replace("(.+.+)", "")

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.command == "markov" and message.user.name in self.bot.admins:
            available_brains = os.listdir(os.path.join("hubbot", "data", "brains"))
            available_brains = sorted([brain.split(".")[0] for brain in available_brains if brain.endswith(".brain")])

            if len(message.parameter_list) == 2 and message.parameter_list[0].lower() == "banword":
                self._add_banned_word(message.parameter_list[1])
                return IRCResponse(ResponseType.SAY,
                                   "Alright, {} will now no longer generate Markov replies containing that word.".format(self.bot.nickname),
                                   message.reply_to)

            elif len(message.parameter_list) == 2 and message.parameter_list[0].lower() == "banregex":
                self._add_banword_regex(message.parameter_list[1])
                return IRCResponse(ResponseType.SAY,
                                   "Alright, {} will now no longer generate Markov replies matching that regex.".format(self.bot.nickname),
                                   message.reply_to)

            elif len(message.parameter_list) == 2 and message.parameter_list[0].lower() == "load":
                if message.parameter_list[1] in available_brains:
                    self.brain = None
                    self.brain = Brain(os.path.join("hubbot", "data", "brains", "{}.brain".format(message.parameter_list[1])))
                    self.brain_file = message.parameter_list[1]
                    return IRCResponse(ResponseType.SAY, "Successfully loaded markov brain {}".format(self.brain_file), message.reply_to)
                else:
                    return IRCResponse(ResponseType.SAY, "That's not a brain that I have on file.", message.reply_to), \
                           IRCResponse(ResponseType.NOTICE, "Available brains are: {}".format(", ".join(available_brains)), message.user.name)

            elif len(message.parameter_list) == 1 and message.parameter_list[0].lower() == "unload":
                self.brain = None
                old_name = self.brain_file
                self.brain_file = ""
                return IRCResponse(ResponseType.SAY, "Successfully unloaded markov brain {}".format(old_name), message.reply_to)

            else:
                return IRCResponse(ResponseType.SAY,
                                   "Current loaded brain is {}".format(self.brain_file),
                                   message.reply_to), \
                       IRCResponse(ResponseType.NOTICE,
                                   "Available brains are: {}".format(", ".join(available_brains)),
                                   message.user.name)

        elif message.user.name == self.bot.nickname:
            return
        elif message.target_type is TargetTypes.USER and message.command not in self.bot.module_handler.mapped_triggers:
            reply = self._generate_clean_reply(message.message_string)
            return IRCResponse(ResponseType.SAY, reply.capitalize(), message.reply_to)
        elif self.bot.nickname.lower() in message.message_string.lower() and len(message.message_list) > 1:
            # remove the bot's nick from the message before generating a reply
            message_list = [item for item in message.message_list if item.lower() != self.bot.nickname.lower()]
            nick_list = [nick.lower() for nick in self.bot.channels[message.reply_to].users.keys()]
            reply = self._generate_clean_reply(" ".join(message_list), user_nick=message.user.name, replace_nicks=nick_list)
            return IRCResponse(ResponseType.SAY, reply.capitalize(), message.reply_to)
        elif message.type == "PRIVMSG":
            if self.brain_file == self.bot.network:
                message_list = [item.lower() for item in message.message_list if item.lower() != self.bot.nickname.lower()]
                self.add_to_brain(" ".join(message_list))
