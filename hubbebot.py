import sys, platform, os, traceback, datetime, codecs
from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor

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

    def signedOn(self):
        for channel in GlobalVars.channels:
            self.join(channel)
    
    def privmsg(self, user, channel, msg):
        message = IRCMessage('PRIVMSG', user, channel, msg)
        self.handleMessage(message)

    def action(self, user, channel, msg):
        message = IRCMessage('ACTION', user, channel, msg)
        self.handleMessage(message)
    
    def noticed(self, user, channel, msg):
        message = IRCMessage('NOTICE', user, channel, msg)
        self.handleMessage(message)

    def nickChanged(self, nick):
        self.nickname = nick
        GlobalVars.CurrentNick = nick
    
    def irc_JOIN(self, prefix, params):
        message = IRCMessage('JOIN', prefix, params[0], '')
    
    def irc_PART(self, prefix, params):
        partMessage = u''
        if len(params) > 1:
            partMessage = u', message: '+u' '.join(params[1:])
        message = IRCMessage('PART', prefix, params[0], partMessage)

    def sendResponse(self, response):
        if (response == None or response.Response == None):
            return False
        
        if (response.Type == ResponseType.Say):
            self.msg(response.Target, response.Response.encode('utf-8'))
        elif (response.Type == ResponseType.Do):
            self.describe(response.Target, response.Response.encode('utf-8'))
        elif (response.Type == ResponseType.Notice):
            self.notice(response.Target, response.Response.encode('utf-8'))
        elif (response.Type == ResponseType.Raw):
            self.sendLine(response.Response.encode('utf-8'))

    def handleMessage(self, message):
        for (name, func) in GlobalVars.functions.items():
            try:
                response = func.GetResponse(message)
                if response is None:
                    continue
                if hasattr(response, '__iter__'):
                    for r in response:
                        self.responses.append(r)
                else:
                    self.responses.append(response)
            except Exception:
                print "Python Execution Error in '%s': %s" % (name, str( sys.exc_info() ))
        
        for response in self.responses:
            self.sendResponse(response)
        self.responses = []

class HubbeBotFactory(protocol.ClientFactory):
	
	protocol = HubbeBot
	
	def clientConnectionLost(self, connector, reason):
		connector.connect()
		
	def clientConnectionFailed(self, connector, reason):
		print "Connection failed: ", reason
		reactor.stop
		
if __name__ == "__main__":
	AutoLoadFunctions()
	hubbot = HubbeBotFactory()
	reactor.connectTCP(GlobalVars.server, GlobalVars.port, hubbot)
	reactor.run()
