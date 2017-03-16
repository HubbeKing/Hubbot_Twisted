from __future__ import unicode_literals
from twisted.internet import reactor
from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface
from pytimeparse.timeparse import timeparse


class Timer(ModuleInterface):
    triggers = ["timer"]
    help = "timer <time> - starts a countdown timer and notifies you when time's up. No decimals in months or years, max 1 year."

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        flag = False
        if len(message.parameter_list) == 1:
            try:
                delay = int(message.parameter_list[0])
                flag = True
            except:
                delay = timeparse(message.parameter_list[0])
        else:
            delay = timeparse(" ".join(message.parameter_list))
        if delay <= 0 or delay is None:
            return IRCResponse(ResponseType.SAY, "I don't think I understand that...", message.reply_to)
        elif delay > (60 * 60 * 24 * 365):
            return IRCResponse(ResponseType.SAY, "Do you really need a timer that long?", message.reply_to)
        elif delay <= 1:
            return IRCResponse(ResponseType.SAY, "Your timer is up now, {}.".format(message.user.name), message.reply_to)

        else:
            reactor.callLater(delay, self.notify_user, flag, message)
            if flag:
                return IRCResponse(ResponseType.SAY, "{}: A {} second timer has been started!".format(message.user.name, message.parameter_list[0]), message.reply_to)
            else:
                return IRCResponse(ResponseType.SAY, "{}: A {} timer has been started!".format(message.user.name, " ".join(message.parameter_list)), message.reply_to)

    def notify_user(self, flag, message):
        """
        @type flag: bool
        @type message: hubbot.message.IRCMessage
        """
        if flag:
            self.bot.module_handler.send_response(IRCResponse(ResponseType.SAY, "{}: Your {} second timer is up!".format(message.user.name, message.parameter_list[0]), message.reply_to))
        else:
            self.bot.module_handler.send_response(IRCResponse(ResponseType.SAY, "{}: Your {} timer is up!".format(message.user.name, " ".join(message.parameter_list)), message.reply_to))
