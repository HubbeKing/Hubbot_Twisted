from __future__ import unicode_literals
from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel


class Nick(ModuleInterface):
    triggers = ["nick"]
    help = "nick <nick> - changes the bot's nick to the one specified"
    access_level = ModuleAccessLevel.ADMINS
    
    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.parameter_list) > 0:
            return IRCResponse(ResponseType.RAW, "NICK {}".format(message.parameter_list[0]), '')
        else:
            return IRCResponse(ResponseType.SAY, "Change my {} to what?".format(message.command), message.reply_to)
