from twisted.internet import reactor
from hubbot.message import TargetTypes
from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
from cobe_hubbot.mariadb_brain import MariaDBBrain
from cobe_hubbot.sqlite_brain import SQLiteBrain
import os
import re
import sqlite3
import unicodedata


class Markov(ModuleInterface):
    accepted_types = ["PRIVMSG", "ACTION"]

    def __init__(self, bot):
        self.brain = None
        self.brain_file = ""
        self.banword_regexes = []
        self.banwords_regex = re.compile(r"(?!)")
        # should match against nothing, making sure replies are still generated if we have no banned words
        super(Markov, self).__init__(bot)

    def help(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        help_dict = {
            "banword": "{}markov banword <word> - Ban a word from the bot, meaning any replies containing it will be discarded.".format(self.bot.command_char),
            "banregex": "{}markov banregex <regex> - Ban a word or phrase from the bot using regex - any reply matching the regex will be discarded.".format(self.bot.command_char),
            "clearbans": "{}markov clearbans - Remove all banned words and phrases. The bot is now free to generate replies containing anything.".format(self.bot.command_char)
        }
        if len(message.parameter_list) == 1:
            return "Markov - Markov chain replies. Generates replies when bot nick is mentioned. Subcommands: {}".format(", ".join(help_dict.keys()))
        else:
            subcommand = message.parameter_list[1].lower()
            if subcommand in help_dict:
                return help_dict[subcommand]
            return "Markov - Markov chain replies. Generates replies when bot nick is mentioned. Subcommands: {}".format(", ".join(help_dict.keys()))

    def on_load(self):
        if self.bot.network is not None:
            brain_host = os.environ.get("MYSQL_HOST", None)
            brain_user = os.environ.get("MYSQL_USER", None)
            brain_password = os.environ.get("MYSQL_PASSWORD", None)
            if None not in (brain_host, brain_user, brain_password):
                self.bot.logger.info("Connecting to {!r} for brain database...".format(brain_host))
                self.brain = MariaDBBrain(brain_name=self.bot.network,
                                          mariadb_host=brain_host,
                                          mariadb_user=brain_user,
                                          mariadb_password=brain_password)
            else:
                # fallback to sqlite3 brain
                self.bot.logger.warning("Markov is using SQLite fallback brain!")
                self.brain = SQLiteBrain(filename=os.path.join("data", "brains", "{}.brain".format(self.bot.network)))
            self._init_banwords_db()
            self._load_banwords_regexes()
            self.bot.logger.info("Markov module loaded successfully.")
        else:
            self.bot.logger.info("Markov module could not get network name, delaying load...")
            self.bot.module_handler.unload_module("Markov")
            reactor.callLater(5.0, self.bot.module_handler.load_module, "Markov")

    def _init_banwords_db(self):
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

    def _clear_banword_regexes(self):
        self.banword_regexes = []
        self.banwords_regex = re.compile(r"(?!)", re.IGNORECASE)
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM markov_banwords_regexes")
            conn.commit()

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
        attempts = 0
        while len(reply.split()) < 2 or self.banwords_regex.search(reply):
            if attempts >= 50:
                # if we fail to generate a good reply after 50 attempts, stop trying
                reply = "My brain appears to have broken a bit, let my owner know and they can try to fix that."
                break
            reply = self.brain.reply(message_string, max_len=max_len)
            reply = self._clean_up_string(reply)
            if replace_nicks is not None:
                for nick in replace_nicks:
                    # check if any of the nicks in replace_nicks are in the reply and replace them with user_nick if so
                    if nick in reply.lower():
                        reply_list = reply.lower().split()
                        nick_index = self._index_containing_substring(reply_list, nick)
                        new_list = [item for item in reply_list if nick not in item]
                        new_list.insert(nick_index, user_nick)
                        reply = " ".join(new_list)
            attempts += 1
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

            elif len(message.parameter_list) == 1 and message.parameter_list[0].lower() == "clearbans":
                self._clear_banword_regexes()
                return IRCResponse(ResponseType.SAY,
                                   "All banned words and regexes have now been removed.",
                                   message.reply_to)
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
