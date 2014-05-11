from IRCResponse import IRCResponse, ResponseType
from Function import Function
import re


class Instantiate(Function):
    Help = 'join <channel> - makes the bot join the specified channel(s)'

    def GetResponse(self, HubbeBot, message):
        if message.Type != 'PRIVMSG':
            return
        
        match = re.search('^join$', message.Command, re.IGNORECASE)
        if not match:
            return
        
        if len(message.ParameterList) > 0:
            responses = []
            for param in message.ParameterList:
                channel = param
                if not channel.startswith('#'):
                    channel = '#' + channel
                responses.append(IRCResponse(ResponseType.Raw, 'JOIN {}'.format(channel), ''))
                HubbeBot.channels.append(channel)
            return responses
        else:
            return IRCResponse(ResponseType.Say, "{}, you didn't say where I should join".format(message.User.Name), message.ReplyTo)