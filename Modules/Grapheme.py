from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType
import GlobalVars


class Module(ModuleInterface):
    help = "grapheme -- for when you need someone to talk to."

    def shouldTrigger(self, message):
        if message.Type == "PRIVMSG" and message.MessageList[0].lower().startswith(GlobalVars.CurrentNick.lower()) and len(message.MessageList) > 1:
            return True
        else:
            return False

    def onTrigger(self, Hubbot, message):
        stringToUse = " ".join(message.MessageList[1:])
        messageToUse = stringToUse.encode("utf-8")
        Hubbot.learnMessage(messageToUse)
        reply = Hubbot.brain.respond(messageToUse)
        if "." in reply:
            reply = reply[:180].rsplit(".", 1)[0]
        else:
            reply = reply[:180].rsplit(" ", 1)[0]
        if len(reply) > 180:
            reply = reply[:181]
        reply = reply.encode("utf-8", "ignore")
        return IRCResponse(ResponseType.Say, reply, message.ReplyTo)
