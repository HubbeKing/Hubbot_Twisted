import sys, platform, os, traceback, datetime, codecs
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor
import re

from IRCResponse import IRCResponse, ResponseType
from IRCMessage import IRCMessage
from FunctionHandler import AutoLoadFunctions
import GlobalVars

class HubbeBot(irc.IRCClient):

    nickname = GlobalVars.CurrentNick
    
    realname = GlobalVars.CurrentNick
    username = GlobalVars.CurrentNick
    
    fingerReply = GlobalVars.finger
    
    versionName = GlobalVars.CurrentNick
    versionNum = GlobalVars.version
    versionEnv = platform.platform()
    
    sourceURL = GlobalVars.source
    
    responses = []

    def __init__(self, server, channels):
        self.server = server
        self.channels = channels

    def signedOn(self):
        for channel in self.channels:
            self.join(channel)
    
    def privmsg(self, user, channel, msg):
        message = IRCMessage('PRIVMSG', user, channel, msg)
        if msg.startswith(GlobalVars.CommandChar):
            self.log(u'<{0}> {1}'.format(message.User.Name, message.MessageString), message.ReplyTo)
        self.handleMessage(message)

    def action(self, user, channel, msg):
        message = IRCMessage('ACTION', user, channel, msg)
        pattern = pattern = "hu+g|cuddle|snu+ggle|snu+g|squeeze|glomp"
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
            partMessage = u', message: '+u' '.join(params[1:])
        message = IRCMessage('PART', prefix, params[0], partMessage)
        self.handleMessage(message)

    def irc_QUIT(self, prefix, params):
        message = IRCMessage('QUIT', prefix, params[0], '')
        self.handleMessage(message)

    def sendResponse(self, response):
        if (response == None or response.Response == None):
            return False
        
        if (response.Type == ResponseType.Say):
            self.msg(response.Target, response.Response.encode('utf-8'))
            self.log(u'<{0}> {1}'.format(self.nickname, response.Response), response.Target)
        elif (response.Type == ResponseType.Do):
            self.describe(response.Target, response.Response.encode('utf-8'))
            self.log(u'*{0} {1}*'.format(self.nickname, response.Response), response.Target)
        elif (response.Type == ResponseType.Notice):
            self.notice(response.Target, response.Response.encode('utf-8'))
            self.log(u'[{0}] {1}'.format(self.nickname, response.Response), response.Target)
        elif (response.Type == ResponseType.Raw):
            self.sendLine(response.Response.encode('utf-8'))

    def handleMessage(self, message):
        self.responses = [] # in case earlier Function responses caused some weird errors
        for (name, func) in GlobalVars.functions.items():
            try:
                response = func.GetResponse(self, message)
                if response is None:
                    continue
                if hasattr(response, '__iter__'):
                    for r in response:
                        self.responses.append(r)
                else:
                    self.responses.append(response)
            except Exception:
                print "Python Execution Error in '%s': %s" % (name, str( sys.exc_info() ))
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
        
class HubbeBotFactory(protocol.ReconnectingClientFactory):

    def __init__(self, server, channels):
        AutoLoadFunctions()
        self.protocol = HubbeBot(server,channels)
        reactor.connectTCP(server, GlobalVars.port, self)
            
    def startedConnecting(self, connector):
        print "-#- Started to connect."

    def buildProtocol(self, addr):
        print "-#- Connected."
        print "-#- Resetting reconnectiong delay"
        self.resetDelay()
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        print "-!- Connection lost. Reason:", reason
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print "-!- Connection failed. Reason:", reason
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
