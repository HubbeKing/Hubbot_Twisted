from hubbot.Utils.stringutils import delta_time_to_string
from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
import datetime


class Uptime(ModuleInterface):
    triggers = ["uptime"]
    help = "uptime -- returns the uptime for the bot"

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        now = datetime.datetime.now()
        time_delta = now - self.bot.startTime
        return IRCResponse(ResponseType.SAY, "I have been running for {}!".format(delta_time_to_string(time_delta, resolution="s")), message.reply_to)
