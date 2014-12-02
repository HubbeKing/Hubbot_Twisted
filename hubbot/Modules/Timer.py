from twisted.internet import reactor
from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface
from timeparse import timeparse


class Timer(ModuleInterface):
    triggers = ["timer"]
    help = "timer <time> - starts a countdown timer and notifies you when time's up. No decimals in months or years, max 1 year."

    def onTrigger(self, message):
        flag = False
        if len(message.ParameterList) == 1:
            try:
                delay = int(message.ParameterList[0])
                flag = True
            except:
                delay = timeparse(message.ParameterList[0])
        else:
            delay = timeparse(" ".join(message.ParameterList))
        if delay <= 0 or delay is None:
            return IRCResponse(ResponseType.Say, "I don't think I understand that...", message.ReplyTo)
        elif delay > (60 * 60 * 24 * 365):
            return IRCResponse(ResponseType.Say, "Do you really need a timer that long?", message.ReplyTo)
        elif delay <= 1:
            return IRCResponse(ResponseType.Say, "Your timer is up now, {}.".format(message.User.Name), message.ReplyTo)

        else:
            reactor.callLater(delay, self.notifyUser, flag, message)
            if flag:
                return IRCResponse(ResponseType.Say, "{}: A {} second timer has been started!".format(message.User.Name, message.ParameterList[0]), message.ReplyTo)
            else:
                return IRCResponse(ResponseType.Say, "{}: A {} timer has been started!".format(message.User.Name," ".join(message.ParameterList)), message.ReplyTo)

    def notifyUser(self, flag, message):
        if flag:
            self.bot.moduleHandler.sendResponse(IRCResponse(ResponseType.Say, "{}: Your {} second timer is up!".format(message.User.Name, message.ParameterList[0]), message.ReplyTo))
        else:
            self.bot.moduleHandler.sendResponse(IRCResponse(ResponseType.Say, "{}: Your {} timer is up!".format(message.User.Name, " ".join(message.ParameterList)), message.ReplyTo))
