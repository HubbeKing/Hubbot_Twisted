from twisted.internet import reactor
from IRCResponse import IRCResponse, ResponseType
from CommandInterface import CommandInterface
from timeparse import timeparse


class Command(CommandInterface):
    triggers = ["timer"]
    help = "timer <time> - starts a countdown timer and notifies you when time's up. Max 1yrs0mths0w0d0h0m0s"

    def execute(self, Hubbot, message):
        flag = False
        if len(message.ParameterList) != 1:
            return IRCResponse(ResponseType.Say, "Please use only 1 argument.", message.ReplyTo)
        try:
            delay = int(message.ParameterList[0])
            flag = True
        except:
            delay = timeparse(message.ParameterList[0])
        if delay <= 0 or delay == None:
            return IRCResponse(ResponseType.Say, "I don't think I understand that...", message.ReplyTo)
        elif delay > (60 * 60 * 24 * 365):
            return IRCResponse(ResponseType.Say, "Do you really need a timer that long?", message.ReplyTo)
        elif delay < 1:
            return IRCResponse(ResponseType.Say, "Less than a second? Really?", message.ReplyTo)

        else:
            reactor.callLater(delay, Hubbot.notifyUser, flag, message)
            if flag:
                return IRCResponse(ResponseType.Say, "{}: A {} second timer has been started!".format(message.User.Name, message.ParameterList[0]), message.ReplyTo)
            else:
                return IRCResponse(ResponseType.Say, "{}: A {} timer has been started!".format(message.User.Name,message.ParameterList[0]), message.ReplyTo)