import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import platform

from twisted.words.protocols import irc

from hubbot import __version__
from hubbot.channel import IRCChannel
from hubbot.message import IRCMessage
from hubbot.modulehandler import ModuleHandler
from hubbot.user import IRCUser


class Hubbot(irc.IRCClient):
    sourceURL = "https://github.com/HubbeKing/Hubbot_Twisted"

    def __init__(self, factory, config):
        """
        @type factory: hubbot.factory.HubbotFactory
        @type config: hubbot.config.Config
        """
        self.config = config
        self.factory = factory
        self.address = config["address"]
        self.port = config.item_with_default("port", 6667)
        self.nickname = config.item_with_default("nickname", "Hubbot")
        self.username = config.item_with_default("username", self.nickname)
        self.realname = config.item_with_default("realname", self.nickname)
        self.password = config.item_with_default("password", None)
        self.versionName = self.nickname
        self.versionNum = __version__
        self.versionEnv = platform.platform()
        self.channel_list = config.item_with_default("channels", [])
        self.command_char = config.item_with_default("command_char", "!")

        self.logger = None
        self.setup_logging()
        self.database_file = os.path.join("hubbot", "data", "data.db")
        self.admins = []
        self.ignores = []

        self.network = None
        self.hostname = None
        self.prefixes_char_to_mode = {}
        self.user_modes = {}
        self.channels = {}

        self.quitting = False
        self.start_time = datetime.datetime.utcnow()
        self.module_handler = ModuleHandler(self)
        self.module_handler.load_all_modules()

    def signedOn(self):
        for channel in self.channel_list:
            self.join(channel)

    def join(self, channel, key=None):
        self.channels[channel] = IRCChannel(channel)
        irc.IRCClient.join(self, channel, key)

    def isupport(self, options):
        for item in options:
            if "=" in item:
                option = item.split("=")
                if option[0] == "PREFIX":
                    prefixes = option[1]
                    status_modes = prefixes[:prefixes.find(")")]
                    status_chars = prefixes[prefixes.find(")"):]
                    for i in range(1, len(status_modes)):
                        self.prefixes_char_to_mode[status_chars[i]] = status_modes[i]
                elif option[0] == "NETWORK":
                    self.network = option[1]
                    self.logger.info("Network is {!r}".format(self.network))

    def irc_RPL_NAMREPLY(self, prefix, params):
        channel = self.get_channel(params[2])

        if channel.names_list_complete:
            channel.names_list_complete = False
            channel.users.clear()
            channel.ranks.clear()

        channel_users = params[3].split(" ")
        for channel_user in channel_users:
            if channel_user == "":
                continue
            rank = ""
            if channel_user[0] in self.prefixes_char_to_mode:
                rank = self.prefixes_char_to_mode[channel_user[0]]
                channel_user = channel_user[1:]
            if channel_user not in channel.users:
                user = IRCUser("{}!{}@{}".format(channel_user, "none", "none"))
            else:
                user = channel.users[channel_user]

            channel.users[user.name] = user
            channel.ranks[user.name] = rank

    def irc_RPL_ENDOFNAMES(self, prefix, params):
        channel = self.get_channel(params[1])
        channel.names_list_complete = True

    def irc_RPL_YOURHOST(self, prefix, params):
        for word in params[0]:
            if "," in word:
                self.hostname = word.rstrip(",")
        self.logger.info("Host is {!r}".format(self.hostname))

    def irc_NICK(self, prefix, params):
        user_array = prefix.split("!")
        oldnick = user_array[0]
        newnick = params[0]

        for key in self.channels:
            channel = self.channels[key]
            for user_key in channel.users:
                user = channel.users[user_key]
                if user_key == oldnick:
                    channel.users[newnick] = IRCUser("{}!{}@{}".format(newnick, user.user, user.hostmask))
                    del channel.users[oldnick]
                    if oldnick in channel.ranks:
                        channel.ranks[newnick] = channel.ranks[oldnick]
                        del channel.ranks[oldnick]
                    message = IRCMessage("NICK", prefix, channel, newnick, self)
                    self.module_handler.handle_message(message)

    def irc_JOIN(self, prefix, params):
        channel = self.get_channel(params[0])
        message = IRCMessage("JOIN", prefix, channel, "", self)

        if message.user.name != self.nickname:
            channel.users[message.user.name] = message.user
        self.module_handler.handle_message(message)

    def irc_PART(self, prefix, params):
        part_message = ""
        if len(params) > 1:
            part_message = ", message: {}".format(" ".join(param.decode(encoding="utf-8", errors="ignore") for param in params[1:]))
        channel = self.get_channel(params[0])
        if channel is None:
            channel = IRCChannel(params[0])
        message = IRCMessage("PART", prefix, channel, part_message, self)

        if message.user.name != self.nickname:
            del channel.users[message.user.name]
            if message.user.name in channel.ranks:
                del channel.ranks[message.user.name]

        self.module_handler.handle_message(message)

    def irc_KICK(self, prefix, params):
        kick_message = ""
        if len(params) > 2:
            kick_message = ", message: {}".format(" ".join(param.decode(encoding="utf-8", errors="ignore") for param in params[2:]))

        channel = self.get_channel(params[0])
        message = IRCMessage("KICK", prefix, channel, kick_message, self)
        message.kickee = params[1]
        if message.kickee == self.nickname:
            del self.channels[message.reply_to]
        else:
            del channel.users[message.kickee]
            if message.kickee in channel.ranks:
                del channel.ranks[message.kickee]
        self.module_handler.handle_message(message)

    def irc_QUIT(self, prefix, params):
        quit_message = ""
        if len(params) > 0:
            quit_message = ", message: {}".format(" ".join(param.decode(encoding="utf-8", errors="ignore") for param in params[0:]))
        for key in self.channels:
            channel = self.channels[key]
            message = IRCMessage("QUIT", prefix, channel, quit_message, self)
            if message.user.name in channel.users:
                del channel.users[message.user.name]
                if message.user.name in channel.ranks:
                    del channel.ranks[message.user.name]
            self.module_handler.handle_message(message)

    def irc_ERRROR(self, prefix, params):
        self.logger.error(" ".join(params))

    def nickChanged(self, nick):
        self.logger.info("Nick changed from {!r} to {!r}".format(self.nickname, nick))
        self.nickname = nick

    def privmsg(self, user, channel, message):
        msg = IRCMessage("PRIVMSG", user, self.get_channel(channel), message, self)
        self.module_handler.handle_message(msg)

    def action(self, user, channel, data):
        msg = IRCMessage("ACTION", user, self.get_channel(channel), data, self)
        self.module_handler.handle_message(msg)

    def noticed(self, user, channel, message):
        msg = IRCMessage("NOTICE", user, self.get_channel(channel), message.upper(), self)
        self.module_handler.handle_message(msg)

    def get_channel(self, channel_name):
        if channel_name in self.channels:
            return self.channels[channel_name]
        else:
            return None

    def setup_logging(self):
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        log_path = os.path.join(dname, "logs")
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        logger = logging.getLogger("bot")
        handler = TimedRotatingFileHandler(os.path.join(log_path, "{}.log".format(self.address)), when="midnight",
                                           backupCount=7)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%H:%M:%S'))
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)

        self.logger = logger
