from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface


class Triggers(ModuleInterface):
    triggers = ["triggers"]
    help = "triggers -- returns a list of all command triggers, must be over PM"

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.User.Name != message.ReplyTo:
            return IRCResponse(ResponseType.Say, "{} must be used over PM!".format(message.Command), message.ReplyTo)
        else:
            response = ", ".join(sorted(self.bot.moduleHandler.mappedTriggers.keys()))
            return IRCResponse(ResponseType.Say, response, message.ReplyTo)
