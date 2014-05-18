import sys, platform, os, traceback, datetime, codecs, re
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor
from megahal import *
from IRCResponse import ResponseType, IRCResponse
from IRCMessage import IRCMessage, IRCUser, IRCChannel
import GlobalVars


class Hubbot(irc.IRCClient):
    nickname = GlobalVars.CurrentNick

    realname = GlobalVars.CurrentNick
    username = GlobalVars.CurrentNick

    fingerReply = GlobalVars.finger

    versionName = GlobalVars.CurrentNick
    versionNum = GlobalVars.version
    versionEnv = platform.platform()

    sourceURL = GlobalVars.source

    responses = []

    startTime = datetime.datetime.min

    def __init__(self, server, channels):
        self.server = server
        self.channels = channels
        self.Quitting = False
        self.startTime = datetime.datetime.now()
        self.brain = MegaHAL(None,"data/{}.brain".format(server),None)

    def signedOn(self):
        for channel in self.channels.keys():
            if channel is not GlobalVars.CurrentNick and channel is not "Auth":
                self.join(channel)

    def irc_RPL_NAMREPLY(self, prefix, params):
        channel = self.channels[params[2]]
        modes = ["+", "@", "~"]

        if channel.NamesListComplete:
            channel.NamesListComplete = False
            channel.Users.clear()

        channelUsers = params[3].split(" ")
        for channelUser in channelUsers:
            if channelUser != "" and channelUser[0] in modes:
                channelUser = channelUser[1:]

            user = self.getUser(channel, channelUser)
            if not user:
                user = IRCUser("{}!{}@{}".format(channelUser, "none", "none"))

            channel.Users[user.Name] = user

    def irc_RPL_ENDOFNAMES(self, prefix, params):
        channel = self.channels[params[1]]
        channel.NamesListComplete = True

    def privmsg(self, user, channel, msg):
        message = IRCMessage('PRIVMSG', user, self.channels[channel], msg)
        msgList = msg.split(" ")
        msgToUse = ""
        for msg in msgList:
            if GlobalVars.CurrentNick not in msg:
                msgToUse += msg + " "
        msgToUse.rstrip()
        if "http" not in msgToUse:
            self.brain.learn(msgToUse)
            self.brain.sync()
        for (name, module) in GlobalVars.modules.items():
            if message.Command in module.triggers:
                self.log(u'<{0}> {1}'.format(message.User.Name, message.MessageString), message.ReplyTo)
        self.handleMessage(message)

    def action(self, user, channel, msg):
        message = IRCMessage('ACTION', user, self.channels[channel], msg)
        pattern = "hu+g|cuddle|snu+ggle|snu+g|squeeze|glomp"
        match = re.search(pattern, msg, re.IGNORECASE)
        if match:
            self.log(u'*{0} {1}*'.format(message.User.Name, message.MessageString), message.ReplyTo)
        self.handleMessage(message)

    def noticed(self, user, channel, msg):
        message = IRCMessage('NOTICE', user, self.channels[channel], msg.upper())
        self.log(u'[{0}] {1}'.format(message.User.Name, message.MessageString), message.ReplyTo)
        self.handleMessage(message)

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
                    message = IRCMessage('NICK', prefix, channel, newnick)
                    self.handleMessage(message)

    def nickChanged(self, nick):
        self.nickname = nick
        GlobalVars.CurrentNick = nick

    def irc_JOIN(self, prefix, params):
        channel = self.channels[params[0]]
        message = IRCMessage('JOIN', prefix, channel, '')

        if message.User.Name != GlobalVars.CurrentNick:
            channel.Users[message.User.Name] = message.User
        self.handleMessage(message)

    def irc_PART(self, prefix, params):
        partMessage = u''
        if len(params) > 1:
            partMessage = u', message: ' + u' '.join(params[1:])
        if params[0] in self.channels.keys():
            channel = self.channels[params[0]]
        else:
            channel = IRCChannel(params[0])
        message = IRCMessage('PART', prefix, channel, partMessage)

        if message.User.Name != GlobalVars.CurrentNick:
            del channel.Users[message.User.Name]
        self.handleMessage(message)

    def irc_KICK(self, prefix, params):
        kickMessage = u''
        if len(params) > 2:
            kickMessage = u', message: ' + u' '.join(params[2:])

        channel = self.channels[params[0]]
        message = IRCMessage('KICK', prefix, channel, kickMessage)
        kickee = params[1]
        if kickee == GlobalVars.CurrentNick:
            del self.channels[message.ReplyTo]
        else:
            del channel.Users[kickee]
        self.handleMessage(message)

    def irc_QUIT(self, prefix, params):
        quitMessage = u''
        if len(params) > 0:
            quitMessage = u', message: ' + u' '.join(params[0:])
        for key in self.channels:
            channel = self.channels[key]
            message = IRCMessage('QUIT', prefix, channel, quitMessage)
            if message.User.Name in channel.Users:
                del channel.Users[message.User.Name]
            self.handleMessage(message)

    def sendResponse(self, response):
        if response is None or response.Response is None:
            return False

        if response.Type == ResponseType.Say:
            self.msg(response.Target, response.Response.encode('utf-8'))
            self.log(u'<{0}> {1}'.format(self.nickname, response.Response), response.Target)
        elif response.Type == ResponseType.Do:
            self.describe(response.Target, response.Response.encode('utf-8'))
            self.log(u'*{0} {1}*'.format(self.nickname, response.Response), response.Target)
        elif response.Type == ResponseType.Notice:
            self.notice(response.Target, response.Response.encode('utf-8'))
            self.log(u'[{0}] {1}'.format(self.nickname, response.Response), response.Target)
        elif response.Type == ResponseType.Raw:
            self.sendLine(response.Response.encode('utf-8'))

    def handleMessage(self, message):
        self.responses = []  # in case earlier module responses caused some weird errors
        for (name, module) in GlobalVars.modules.items():
            try:
                if module.shouldTrigger(message):
                    response = module.onTrigger(self, message)
                    if response is None:
                        continue
                    if hasattr(response, "__iter__"):
                        for r in response:
                            self.responses.append(r)
                    else:
                        self.responses.append(response)
            except Exception:
                print "Python Execution Error in '%s': %s" % (name, str(sys.exc_info()))
                traceback.print_tb(sys.exc_info()[2])
        for response in self.responses:
            self.sendResponse(response)
        self.responses = []

    def log(self, text, target):
        now = datetime.datetime.now()
        time = now.strftime("[%H:%M]")
        data = u'{0} {1}'.format(time, text)
        print target, data

        fileName = "{0}{1}.txt".format(target, now.strftime("-%Y%m%d"))
        fileDirs = os.path.join(GlobalVars.logPath, self.server)
        if not os.path.exists(fileDirs):
            os.makedirs(fileDirs)
        filePath = os.path.join(fileDirs, fileName)

        with codecs.open(filePath, 'a+', 'utf-8') as f:
            f.write(data + '\n')

    def notifyUser(self, flag, message):
        if flag:
            self.sendResponse(IRCResponse(ResponseType.Say, "{}: Your {} second timer is up!".format(message.User.Name, message.ParameterList[0]), message.ReplyTo))
        else:
            self.sendResponse(IRCResponse(ResponseType.Say, "{}: Your {} timer is up!".format(message.User.Name, message.ParameterList[0]), message.ReplyTo))

    def getUser(self, channel, nickname):
        if nickname in channel.Users:
            return channel.Users[nickname]
        return None

class HubbotFactory(protocol.ReconnectingClientFactory):
    def __init__(self, server, port, channels):
        self.port = port
        self.protocol = Hubbot(server, channels)
        reactor.connectTCP(server, port, self)

    def startedConnecting(self, connector):
        print "-#- Started to connect."

    def buildProtocol(self, addr):
        print "-#- Connected."
        print "-#- Resetting reconnectiong delay"
        self.resetDelay()
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        if not self.protocol.Quitting:
            print "-!- Connection lost. Reason:", reason
            protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print "-!- Connection failed. Reason:", reason
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
