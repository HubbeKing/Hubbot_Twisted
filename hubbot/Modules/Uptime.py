from hubbot.Utils.stringutils import deltaTimeToString
from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
import datetime


class Uptime(ModuleInterface):
    triggers = ["uptime"]
    help = "uptime -- returns the uptime for the bot"

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        now = datetime.datetime.now()
        timeDelta = now - self.bot.startTime
        return IRCResponse(ResponseType.Say, "I have been running for {}!".format(deltaTimeToString(timeDelta, resolution="s")), message.ReplyTo)
