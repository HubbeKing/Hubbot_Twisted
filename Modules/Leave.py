from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface, ModuleAccessLevels

class Leave(ModuleInterface):
    triggers = ["leave", "gtfo"]
    help = "leave/gtfo - makes the bot leave the current channel"
    accessLevel = ModuleAccessLevels.ADMINS

    def onTrigger(self, message):
        if len(message.ParameterList) > 0:
            del self.bot.channels[message.ReplyTo]
            return IRCResponse(ResponseType.Raw, 'PART {} :{}'.format(message.ReplyTo, message.Parameters), '')
        else:
            del self.bot.channels[message.ReplyTo]
            return IRCResponse(ResponseType.Raw, 'PART {} :toodles!'.format(message.ReplyTo), '')