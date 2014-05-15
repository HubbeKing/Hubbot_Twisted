from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType
import GlobalVars


class Module(ModuleInterface):
    help = "grapheme -- for when you need someone to talk to."

    def shouldTrigger(self, message):
        if message.MessageList[0].startswith(GlobalVars.CurrentNick) and len(message.MessageList) > 1:
            return True
        else:
            return False

    def onTrigger(self, Hubbot, message):
        messageToUse = " ".join(message.MessageList[1:])
        return IRCResponse(ResponseType.Say, Hubbot.brain.get_reply(messageToUse), message.ReplyTo)
