from __future__ import unicode_literals
from hubbot.channel import IRCChannel
from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface


class Join(ModuleInterface):
    triggers = ["join"]
    help = 'join <channel> - makes the bot join the specified channel(s)'

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.parameter_list) > 0:
            responses = []
            for param in message.parameter_list:
                channel = param
                if not channel.startswith('#'):
                    channel = '#' + channel
                responses.append(IRCResponse(ResponseType.RAW, 'JOIN {}'.format(channel), ''))
                self.bot.channels[channel] = IRCChannel(channel)
            return responses
        else:
            return IRCResponse(ResponseType.SAY, "{}, you didn't say where I should join".format(message.user.name), message.reply_to)
