from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel


class Leave(ModuleInterface):
    triggers = ["leave", "gtfo"]
    help = "leave/gtfo - makes the bot leave the current channel"
    accessLevel = ModuleAccessLevel.ADMINS

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.ParameterList) > 0:
            del self.bot.channels[message.ReplyTo]
            return IRCResponse(ResponseType.Raw, 'PART {} :{}'.format(message.ReplyTo, message.Parameters), '')
        else:
            del self.bot.channels[message.ReplyTo]
            return IRCResponse(ResponseType.Raw, 'PART {} :toodles!'.format(message.ReplyTo), '')
