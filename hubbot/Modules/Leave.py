from __future__ import unicode_literals
from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel


class Leave(ModuleInterface):
    triggers = ["leave", "gtfo"]
    help = "leave/gtfo - makes the bot leave the current channel"
    access_level = ModuleAccessLevel.ADMINS

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.parameter_list) > 0:
            del self.bot.channels[message.reply_to]
            return IRCResponse(ResponseType.RAW, 'PART {} :{}'.format(message.reply_to, message.parameters), '')
        else:
            del self.bot.channels[message.reply_to]
            return IRCResponse(ResponseType.RAW, 'PART {} :toodles!'.format(message.reply_to), '')
