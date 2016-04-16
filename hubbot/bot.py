import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import platform

from twisted.words.protocols import irc

from hubbot import __version__
from hubbot.message import IRCMessage
from hubbot.channel import IRCChannel
from hubbot.user import IRCUser
from hubbot.modulehandler import ModuleHandler


class Hubbot(irc.IRCClient):
    sourceURL = "https://github.com/HubbeKing/Hubbot_Twisted/"

    def __init__(self, server, channels, bothandler):
        """
        @type bothandler: hubbot.bothandler.BotHandler
        """
        self.server = server
        self.channels = channels
        self.bothandler = bothandler

        self.setupLogging()
        self.readConfig()

        self.databaseFile = os.path.join("hubbot", "data", "data.db")
        self.admins = []
        self.ignores = []

        self.Quitting = False
        self.startTime = datetime.datetime.now()

        self.prefixesCharToMode = {"+": "v", "@": "o"}
        self.userModes = {}
        self.moduleHandler = ModuleHandler(self)
        self.moduleHandler.enableAllModules()

    def signedOn(self):
        for channel in self.channels.keys():
            self.join(channel)

    def isupport(self, options):
        for item in options:
            if "=" in item:
                option = item.split("=")
                if option[0] == "PREFIX":
                    prefixes = option[1]
                    statusModes = prefixes[:prefixes.find(")")]
                    statusChars = prefixes[prefixes.find(")"):]
                    for i in range(1, len(statusModes)):
                        self.prefixesCharToMode[statusChars[i]] = statusModes[i]

    def irc_RPL_NAMREPLY(self, prefix, params):
        channel = self.getChannel(params[2])

        if channel.NamesListComplete:
            channel.NamesListComplete = False
            channel.Users.clear()
            channel.Ranks.clear()

        channelUsers = params[3].split(" ")
        for channelUser in channelUsers:
            if channelUser == "":
                continue
            rank = ""
            if channelUser != "" and channelUser[0] in self.prefixesCharToMode:
                rank = self.prefixesCharToMode[channelUser[0]]
                channelUser = channelUser[1:]
            if channelUser not in channel.Users:
                user = IRCUser("{}!{}@{}".format(channelUser, "none", "none"))
            else:
                user = channel.Users[channelUser]

            channel.Users[user.Name] = user
            channel.Ranks[user.Name] = rank

    def irc_RPL_ENDOFNAMES(self, prefix, params):
        channel = self.getChannel(params[1])
        channel.NamesListComplete = True

    def irc_NICK(self, prefix, params):
        userArray = prefix.split("!")
        oldnick = userArray[0]
        newnick = params[0]

        for key in self.channels:
            channel = self.channels[key]
            for userKey in channel.Users:
                user = channel.Users[userKey]
                if userKey == oldnick:
                    channel.Users[newnick] = IRCUser("{}!{}@{}".format(newnick, user.User, user.Hostmask))
                    del channel.Users[oldnick]
                    if oldnick in channel.Ranks:
                        channel.Ranks[newnick] = channel.Ranks[oldnick]
                        del channel.Ranks[oldnick]
                    message = IRCMessage('NICK', prefix, channel, newnick, self)
                    self.moduleHandler.handleMessage(message)

    def irc_JOIN(self, prefix, params):
        channel = self.getChannel(params[0])
        message = IRCMessage('JOIN', prefix, channel, '', self)

        if message.User.Name != self.nickname:
            channel.Users[message.User.Name] = message.User
        self.moduleHandler.handleMessage(message)

    def irc_PART(self, prefix, params):
        partMessage = ""
        if len(params) > 1:
            partMessage = ", message: " + " ".join(params[1:])
        channel = self.getChannel(params[0])
        if channel is None:
            channel = IRCChannel(params[0])
        message = IRCMessage('PART', prefix, channel, partMessage, self)

        if message.User.Name != self.nickname:
            del channel.Users[message.User.Name]
            if message.User.Name in channel.Ranks:
                del channel.Ranks[message.User.Name]
        self.moduleHandler.handleMessage(message)

    def irc_KICK(self, prefix, params):
        kickMessage = ""
        if len(params) > 2:
            kickMessage = ", message: " + " ".join(params[2:])

        channel = self.getChannel(params[0])
        message = IRCMessage('KICK', prefix, channel, kickMessage, self)
        message.Kickee = params[1]
        if message.Kickee == self.nickname:
            del self.channels[message.ReplyTo]
        else:
            del channel.Users[message.Kickee]
            if message.Kickee in channel.Ranks:
                del channel.Ranks[message.Kickee]
        self.moduleHandler.handleMessage(message)

    def irc_QUIT(self, prefix, params):
        quitMessage = ""
        if len(params) > 0:
            quitMessage = ", message: " + " ".join(params[0:])
        for key in self.channels:
            channel = self.channels[key]
            message = IRCMessage('QUIT', prefix, channel, quitMessage, self)
            if message.User.Name in channel.Users:
                del channel.Users[message.User.Name]
                if message.User.Name in channel.Ranks:
                    del channel.Ranks[message.User.Name]
            self.moduleHandler.handleMessage(message)

    def irc_ERROR(self, prefix, params):
        self.logger.error("Error when connecting to server \"{}\" - {}".format(self.server, " ".join(params)))

    def nickChanged(self, nick):
        self.logger.info("Nick changed from \"{}\" to \"{}\".".format(self.nickname, nick))
        self.nickname = nick

    def privmsg(self, user, channel, msg):
        message = IRCMessage('PRIVMSG', user, self.getChannel(channel), msg, self)
        self.moduleHandler.handleMessage(message)

    def action(self, user, channel, msg):
        message = IRCMessage('ACTION', user, self.getChannel(channel), msg, self)
        self.moduleHandler.handleMessage(message)

    def noticed(self, user, channel, msg):
        message = IRCMessage('NOTICE', user, self.getChannel(channel), msg.upper(), self)
        self.moduleHandler.handleMessage(message)

    def setupLogging(self):
        # Setup logs folder
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        logPath = os.path.join(dname, "logs")
        if not os.path.exists(logPath):
            os.makedirs(logPath)

        # Setup the logger and handlers
        logger = logging.getLogger(self.server)
        handler = TimedRotatingFileHandler(os.path.join(logPath, "{}.log".format(self.server)), when="midnight", backupCount=7)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%H:%M:%S'))
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        
        self.logPath = logPath
        self.logger = logger
        
    def readConfig(self):
        self.nickname = self.bothandler.config.serverItemWithDefault(self.server, "nickname", "Hubbot")
        self.username = self.bothandler.config.serverItemWithDefault(self.server, "username", "Hubbot")
        self.realname = self.bothandler.config.serverItemWithDefault(self.server, "realname", "Hubbot")
        self.password = self.bothandler.config.serverItemWithDefault(self.server, "password", None)
        self.versionName = self.nickname
        self.versionNum = __version__
        self.versionEnv = platform.platform()
        self.commandChar = self.bothandler.config.serverItemWithDefault(self.server, "commandchar", "+")
        self.fingerReply = self.bothandler.config.serverItemWithDefault(self.server, "fingerReply", "")

    def getChannel(self, channel):
        if channel in self.channels:
            return self.channels[channel]
        else:
            return None
