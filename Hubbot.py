import sys, platform, os, traceback, datetime, codecs, re
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor
from megahal import *
from IRCResponse import ResponseType, IRCResponse
from IRCMessage import IRCMessage
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
        for channel in self.channels:
            self.join(channel)

    def privmsg(self, user, channel, msg):
        message = IRCMessage('PRIVMSG', user, channel, msg)
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
        message = IRCMessage('ACTION', user, channel, msg)
        pattern = "hu+g|cuddle|snu+ggle|snu+g|squeeze|glomp"
        match = re.search(pattern, msg, re.IGNORECASE)
        if match:
            self.log(u'*{0} {1}*'.format(message.User.Name, message.MessageString), message.ReplyTo)
        self.handleMessage(message)

    def noticed(self, user, channel, msg):
        message = IRCMessage('NOTICE', user, channel, msg.upper())
        self.log(u'[{0}] {1}'.format(message.User.Name, message.MessageString), message.ReplyTo)
        self.handleMessage(message)

    def nickChanged(self, nick):
        self.nickname = nick
        GlobalVars.CurrentNick = nick

    def irc_JOIN(self, prefix, params):
        message = IRCMessage('JOIN', prefix, params[0], '')
        self.handleMessage(message)

    def irc_PART(self, prefix, params):
        partMessage = u''
        if len(params) > 1:
            partMessage = u', message: ' + u' '.join(params[1:])
        message = IRCMessage('PART', prefix, params[0], partMessage)
        self.handleMessage(message)

    def irc_QUIT(self, prefix, params):
        message = IRCMessage('QUIT', prefix, params[0], '')
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
