from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface


class Nick(ModuleInterface):
    triggers = ["nick"]
    help = "nick <nick> - changes the bot's nick to the one specified"
    accessLevel = 1
    
    def onTrigger(self, message):
        """
        @type message: IRCMessage.IRCMessage
        """
        if len(message.ParameterList) > 0:
            return IRCResponse(ResponseType.Raw, "NICK {}".format(message.ParameterList[0]), '')
        else:
            return IRCResponse(ResponseType.Say, "Change my {} to what?".format(message.Command), message.ReplyTo)
