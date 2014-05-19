from enumType import enum
import GlobalVars
import re

TargetTypes = enum('CHANNEL', 'USER')


class IRCChannel(object):
    def __init__(self, name):
        self.Name = name
        self.Users = {}
        self.Ranks = {}
        self.NamesListComplete = True


class IRCUser(object):
    def __init__(self, user):
        self.User = None
        self.Hostmask = None

        if "!" in user:
            userArray = user.split("!")
            self.Name = userArray[0]
            if len(userArray) > 1:
                userArray = userArray[1].split("@")
                self.User = userArray[0]
                self.Hostmask = userArray[1]
            self.String = "{}!{}@{}".format(self.Name, self.User, self.Hostmask)
        else:
            self.Name = user
            self.String = "{}!{}@{}".format(self.Name, "a", "b")


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

    def __init__(self, type, user, channel, message):
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
        elif channel.Name == GlobalVars.CurrentNick:
            self.ReplyTo = self.User.Name
        else:
            self.ReplyTo = channel.Name
        if channel.Name.startswith('#'):
            self.TargetType = TargetTypes.CHANNEL
        else:
            self.TargetType = TargetTypes.USER

        if self.MessageList[0].startswith(GlobalVars.CommandChar):
            self.Command = self.MessageList[0][len(GlobalVars.CommandChar):].lower()
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

    def aliasedMessage(self):
        if self.Command in GlobalVars.commandAliases.keys():
            alias = GlobalVars.commandAliases[self.Command]
            newMsg = re.sub(self.Command, " ".join(alias), self.MessageString, count=1)
            if "$sender" in newMsg:
                newMsg.replace("$sender", self.User.Name)
            if "%channel" in newMsg:
                newMsg.replace("$channel", self.ChannelObj.Name)
            if "%params" in newMsg:
                newMsg.replace("$params", self.Parameters)
            return IRCMessage(self.Type, self.User.String, self.ChannelObj, newMsg)
