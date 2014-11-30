from enumType import enum
from IRCUser import IRCUser

TargetTypes = enum('CHANNEL', 'USER')


class IRCMessage(object):
    Type = None
    User = None
    TargetType = TargetTypes.CHANNEL
    ReplyTo = None
    MessageList = []
    MessageString = None
    ChannelObj = None

    Command = ''
    Parameters = ''
    ParameterList = []

    def __init__(self, type, user, channel, message, bot):
        self.ChannelObj = channel
        try:
            unicodeMessage = message.decode('utf-8', 'ignore')
        except: # Already utf-8, probably.
            unicodeMessage = message
        self.Type = type
        self.MessageList = unicodeMessage.strip().split(' ')
        self.MessageString = unicodeMessage
        self.User = IRCUser(user)
        if user is None or channel is None:
            self.ReplyTo = ""
        elif channel.Name == bot.nickname:
            self.ReplyTo = self.User.Name
        else:
            self.ReplyTo = channel.Name
        if channel.Name.startswith('#'):
            self.TargetType = TargetTypes.CHANNEL
        else:
            self.TargetType = TargetTypes.USER

        if self.MessageList[0].startswith(bot.commandChar):
            self.Command = self.MessageList[0][len(bot.commandChar):].lower()
            if self.Command == "":
                self.Command = self.MessageList[1].lower()
                self.Parameters = u' '.join(self.MessageList[2:])
            else:
                self.Parameters = u' '.join(self.MessageList[1:])

        if self.Parameters.strip():
            self.ParameterList = self.Parameters.split(' ')

            self.ParameterList = [param for param in self.ParameterList if param != '']

            if len(self.ParameterList) == 1 and not self.ParameterList[0]:
                self.ParameterList = []
