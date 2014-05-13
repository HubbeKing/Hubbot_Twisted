from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface
import GlobalVars
import re


class Module(ModuleInterface):
    triggers = ["nick"]
    help = "nick <nick> - changes the bot's nick to the one specified"
    
    def onTrigger(self, Hubbot, message):
        if message.User.Name not in GlobalVars.admins:
            return IRCResponse(ResponseType.Say, "Only my admins can change my name!", message.ReplyTo)
        if len(message.ParameterList) > 0:
            return IRCResponse(ResponseType.Raw, "NICK {}".format(message.ParameterList[0]), '')
        else:
            return IRCResponse(ResponseType.Say, "Change my {} to what?".format(message.Command), message.ReplyTo)