from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType


class Do(ModuleInterface):
    help = "do [channel] <thing> -- do a thing."
    triggers = ["do"]

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say, "Do what?", message.ReplyTo)
        else:
            if message.ParameterList[0].startswith("#"):
                channel = message.ParameterList[0]
                if channel not in self.bot.channels:
                    return IRCResponse(ResponseType.Say, "I am not in \"{}\".".format(channel), message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Do, "{}".format(" ".join(message.ParameterList[1:])), channel)
            else:
                return IRCResponse(ResponseType.Do, "{}".format(" ".join(message.ParameterList)), message.ReplyTo)
