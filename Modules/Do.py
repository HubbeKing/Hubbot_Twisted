from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType


class Do(ModuleInterface):
    help = "do <thing> -- do a thing."
    triggers = ["do"]

    def onTrigger(self, message):
        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say, "Do what?", message.ReplyTo)
        else:
            return IRCResponse(ResponseType.Do, "{}".format(" ".join(message.ParameterList)), message.ReplyTo)