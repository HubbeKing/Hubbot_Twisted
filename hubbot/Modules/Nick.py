from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel


class Nick(ModuleInterface):
    triggers = ["nick"]
    help = "nick <nick> - changes the bot's nick to the one specified"
    accessLevel = ModuleAccessLevel.ADMINS
    
    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.ParameterList) > 0:
            return IRCResponse(ResponseType.Raw, "NICK {}".format(message.ParameterList[0]), '')
        else:
            return IRCResponse(ResponseType.Say, "Change my {} to what?".format(message.Command), message.ReplyTo)
