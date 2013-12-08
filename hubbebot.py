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
        for channel in args[1:]:
            self.join(channel)
    
    def privmsg(self, user, channel, msg):
        message = IRCMessage('PRIVMSG', user, channel, msg)
        self.log(u'<{0}> {1}'.format(message.User.Name, message.MessageString), message.ReplyTo)
        self.handleMessage(message)

    def action(self, user, channel, msg):
        message = IRCMessage('ACTION', user, channel, msg)
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
                traceback.print_tb(sys.exc_info()[2])
				
        for response in self.responses:
            self.sendResponse(response)
        self.responses = []
        
    def log(self, text, target):
        now = datetime.datetime.utcnow()
        time = now.strftime("[%H:%M]")
        data = u'{0} {1}'.format(time, text)
        print target, data
        
        fileName = "{0}{1}.txt".format(target, now.strftime("-%Y%m%d"))
        fileDirs = os.path.join(GlobalVars.logPath, GlobalVars.server)
        if not os.path.exists(fileDirs):
            os.makedirs(fileDirs)
        filePath = os.path.join(fileDirs, fileName)
        
        with codecs.open(filePath, 'a+', 'utf-8') as f:
            f.write(data + '\n')
        
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
	args = sys.argv
	reactor.connectTCP(args[0], GlobalVars.port, hubbot)
	reactor.run()
