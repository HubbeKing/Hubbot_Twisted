from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType
import GlobalVars


class Module(ModuleInterface):
    help = "grapheme -- for when you need someone to talk to."

    def shouldTrigger(self, message):
        if message.messageString.startsWith(GlobalVars.CurrentNick):
            return True
        else:
            return False

    def onTrigger(self, Hubbot, message):
        return IRCResponse(ResponseType.Say, Hubbot.brain.get_reply(message.messageString), message.replyTo)
