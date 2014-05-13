from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface


class Module(ModuleInterface):
    triggers = ["join"]
    help = 'join <channel> - makes the bot join the specified channel(s)'

    def execute(self, Hubbot, message):
        if len(message.ParameterList) > 0:
            responses = []
            for param in message.ParameterList:
                channel = param
                if not channel.startswith('#'):
                    channel = '#' + channel
                responses.append(IRCResponse(ResponseType.Raw, 'JOIN {}'.format(channel), ''))
                Hubbot.channels.append(channel)
            return responses
        else:
            return IRCResponse(ResponseType.Say, "{}, you didn't say where I should join".format(message.User.Name), message.ReplyTo)