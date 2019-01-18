from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface


class Source(ModuleInterface):
    triggers = ["source"]

    def on_load(self):
        self.help = "source - returns a link to {}'s source".format(self.bot.nickname)

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        return IRCResponse(ResponseType.SAY, self.bot.sourceURL, message.reply_to)
