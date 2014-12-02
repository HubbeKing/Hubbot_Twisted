from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType


class Say(ModuleInterface):
    help = "say <thing> -- say a thing."
    triggers = ["say"]

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say, "Say what?", message.ReplyTo)
        else:
            return IRCResponse(ResponseType.Say, "{}".format(" ".join(message.ParameterList)), message.ReplyTo)
