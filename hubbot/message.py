import datetime
from enum import Enum
from hubbot.user import IRCUser


class TargetTypes(Enum):
    CHANNEL = 1
    USER = 2


class IRCMessage(object):
    """
    @type user: hubbot.user.IRCUser
    """

    def __init__(self, message_type, user, channel, message, bot):
        """
        @type channel: hubbot.channel.IRCChannel
        @type bot: hubbot.bot.Hubbot
        """
        try:
            unicode_message = unicode(message, encoding="utf-8", errors="ignore")
        except TypeError:
            unicode_message = message

        self.type = message_type
        self.message_string = unicode_message.encode(encoding="ascii", errors="ignore")
        self.message_list = self.message_string.strip().split(" ")

        self.channel = None
        self.user = None
        if channel is None:
            self.user = IRCUser(user)
            self.channel = None
            self.reply_to = self.user.name
            self.target_type = TargetTypes.USER
        else:
            if user.split("!")[0] in channel.users:
                self.user = channel.users[user.split("!")[0]]
            else:
                self.user = IRCUser(user)
            self.channel = channel
            self.reply_to = channel.name
            self.target_type = TargetTypes.CHANNEL
        self.user.last_active = datetime.datetime.utcnow()

        self.command = ""
        self.parameters = ""
        self.parameter_list = []

        if self.target_type == TargetTypes.USER:
            if self.message_list[0].startswith(bot.command_char):
                self.command = self.message_list[0][len(bot.command_char):].lower()
            else:
                self.command = self.message_list[0].lower()
            if self.command == "":
                self.command = self.message_list[1].lower()
                self.parameters = " ".join(self.message_list[2:])
            else:
                self.parameters = " ".join(self.message_list[1:])

        elif self.message_list[0].startswith(bot.command_char):
            self.command = self.message_list[0][len(bot.command_char):].lower()
            if self.command == "":
                self.command = self.message_list[1].lower()
                self.parameters = " ".join(self.message_list[2:])
            else:
                self.parameters = " ".join(self.message_list[1:])

        if self.parameters.strip():
            self.parameter_list = self.parameters.split(" ")

            self.parameter_list = [param for param in self.parameter_list if param != ""]

            if len(self.parameter_list) == 1 and not self.parameter_list[0]:
                self.parameter_list = []
