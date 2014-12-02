from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType


class Do(ModuleInterface):
    help = "do <thing> -- do a thing."
    triggers = ["do"]

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say, "Do what?", message.ReplyTo)
        else:
            return IRCResponse(ResponseType.Do, "{}".format(" ".join(message.ParameterList)), message.ReplyTo)
