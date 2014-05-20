import sys, traceback
from IRCResponse import IRCResponse, ResponseType
import GlobalVars

class MessageHandler(object):

    def __init__(self, bot):
        """
        @type bot: Hubbot.Hubbot
        """
        self.bot = bot

    def sendResponse(self, response):
        """
        @type response: IRCResponse
        """
        responses = []

        if hasattr(response, "__iter__"):
            for r in response:
                if r is None or r.Response is None or r.Response == "":
                    continue
                responses.append(r)
        elif response is not None and response.Response is not None and response.Response != "":
            responses.append(response)

        for response in responses:
            try:
                if response.Type == ResponseType.Say:
                    self.bot.msg(response.Target, response.Response.encode("utf-8"))
                elif response.Type == ResponseType.Do:
                    self.bot.describe(response.Target, response.Response.encode("utf-8"))
                elif response.Type == ResponseType.Notice:
                    self.bot.notice(response.Target, response.Response.encode("utf-8"))
                elif response.Type == ResponseType.Raw:
                    self.bot.sendLine(response.Response.encode("utf-8"))
            except Exception:
                print "Python Execution Error sending responses '{}': {}".format(responses, str(sys.exc_info()))
                traceback.print_tb(sys.exc_info()[2])


    def handleMessage(self, message):
        """
        @type message: IRCMessage
        """
        for name, module in GlobalVars.modules.iteritems():
            try:
                if module.hasAlias(message):
                    message = message.aliasedMessage()
                if module.shouldTrigger(message):
                    response = module.onTrigger(self.bot, message)
                    if response is None:
                        continue
                    if hasattr(response, "__iter__"):
                        for r in response:
                            self.sendResponse(r)
                    else:
                        self.sendResponse(response)
            except Exception:
                print "Python Execution Error in '{}': {}".format(module.__name__, str(sys.exc_info()))
                traceback.print_tb(sys.exc_info()[2])