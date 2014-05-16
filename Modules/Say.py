from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType


class Module(ModuleInterface):
    help = "say <thing> -- say a thing."
    triggers = ["say"]

    def onTrigger(self, Hubbot, message):
        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say, "Say what?", message.ReplyTo)
        else:
            return IRCResponse(ResponseType.Say, "{}".format(" ".join(message.ParameterList)), message.ReplyTo)