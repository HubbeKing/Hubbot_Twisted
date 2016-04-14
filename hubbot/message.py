import datetime
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

    def __init__(self, messagetype, user, channel, message, bot):
        """
        @type channel: hubbot.channel.IRCChannel
        @type bot: hubbot.bot.Hubbot
        """
        try:
            unicodeMessage = message.decode('utf-8', 'ignore')
        except:  # Already utf-8, probably.
            unicodeMessage = message
        self.Type = messagetype
        self.MessageList = unicodeMessage.strip().split(' ')
        self.MessageString = unicodeMessage

        if channel is None:
            self.User = IRCUser(user)
            self.Channel = None
            self.ReplyTo = self.User.Name
            self.TargetType = TargetTypes.USER
        else:
            if user.split("!")[0] in channel.Users:
                self.User = channel.Users[user]
            else:
                self.User = IRCUser(user)
            self.Channel = channel
            self.ReplyTo = channel.Name
            self.TargetType = TargetTypes.CHANNEL
        self.User.LastActive = datetime.datetime.now()

        if self.MessageList[0].startswith(bot.commandChar):
            self.Command = self.MessageList[0][len(bot.commandChar):].lower()
            if self.Command == "":
                self.Command = self.MessageList[1].lower()
                self.Parameters = ' '.join(self.MessageList[2:])
            else:
                self.Parameters = ' '.join(self.MessageList[1:])

        if self.Parameters.strip():
            self.ParameterList = self.Parameters.split(' ')

            self.ParameterList = [param for param in self.ParameterList if param != '']

            if len(self.ParameterList) == 1 and not self.ParameterList[0]:
                self.ParameterList = []
