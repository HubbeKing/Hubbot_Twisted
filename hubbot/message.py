import re
from enum import Enum
from hubbot.user import IRCUser


class TargetTypes(Enum):
    CHANNEL = 1
    USER = 2


class IRCMessage(object):
    Type = None
    User = None
    ReplyTo = None
    MessageList = []
    MessageString = None

    Command = ''
    Parameters = ''
    ParameterList = []

    def __init__(self, type, user, channel, message, bot):
        """
        @type channel: hubbot.channel.IRCChannel
        @type bot: hubbot.bot.Hubbot
        """
        try:
            unicodeMessage = message.decode('utf-8', 'ignore')
        except:  # Already utf-8, probably.
            unicodeMessage = message
        self.Type = type
        self.MessageList = unicodeMessage.strip().split(' ')
        self.MessageString = unicodeMessage
        self.User = IRCUser(user)

        self.Channel = None
        if channel is None:
            self.ReplyTo = self.User.Name
            self.TargetType = TargetTypes.USER
        else:
            self.Channel = channel
            self.ReplyTo = channel.Name
            self.TargetType = TargetTypes.CHANNEL

        if self.MessageList[0].startswith(bot.commandChar):
            self.Command = self.MessageList[0][len(bot.commandChar):].lower()
            if self.Command == "":
                self.Command = self.MessageList[1].lower()
                self.Parameters = ' '.join(self.MessageList[2:])
            else:
                self.Parameters = ' '.join(self.MessageList[1:])

        elif re.match('{}[:,]?'.format(re.escape(bot.nickname)), self.MessageList[0], re.IGNORECASE):
            if len(self.MessageList) > 1:
                self.Command = self.MessageList[1].lower()
                self.Parameters = u" ".join(self.MessageList[2:])

        if self.Parameters.strip():
            self.ParameterList = self.Parameters.split(' ')

            self.ParameterList = [param for param in self.ParameterList if param != '']

            if len(self.ParameterList) == 1 and not self.ParameterList[0]:
                self.ParameterList = []
