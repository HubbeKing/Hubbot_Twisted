import sqlite3
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel
from hubbot.response import IRCResponse, ResponseType
from pushbullet import PushBullet, InvalidKeyError


class Pushbullet(ModuleInterface):
    triggers = ["pb"]
    accessLevel = ModuleAccessLevel.ADMINS
    help = "pb [title] <text> -- Pushes a pushbullet notification to HubbeKing, title is optional."

    def getAPIkey(self):
        apiKey = None
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT pushbullet FROM keys"):
                apiKey = row[0]
        return apiKey

    def onEnable(self):
        try:
            apiKey = self.getAPIkey()
            if apiKey is not None:
                self.pb = PushBullet(self.getAPIkey())
                self.bot.logger.info("Successfully authenticated with Pushbullet API key.")
            else:
                self.bot.logger.error("Could not fetch Pushbullet API key!")
        except InvalidKeyError:
            self.bot.logger.exception("Pushbullet API key is invalid!")
        except:
            self.bot.logger.exception("Exception when fetching Pushbullet API key!")

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        try:
            if len(message.ParameterList) == 1:
                if "://" not in message.ParameterList[0]:
                    push = self.pb.push_note("From Chat", message.ParameterList[0])
                else:
                    push = self.pb.push_link("From Chat", message.ParameterList[0])
            elif len(message.ParameterList) == 2:
                if "://" not in message.ParameterList[1]:
                    push = self.pb.push_note(message.ParameterList[0], message.ParameterList[1])
                else:
                    push = self.pb.push_link(message.ParameterList[0], message.ParameterList[1])
        except:
            self.bot.logger.exception("Pushbullet push failed!")
            return IRCResponse(ResponseType.Say, "I think something broke, I couldn't send that pushbullet.", message.ReplyTo)
        else:
            if "error" not in push:
                return IRCResponse(ResponseType.Say, "Okay, I'll send that to HubbeKing!", message.ReplyTo)
            else:
                self.bot.logger.error("Pushbullet returned error '{}'".format(push["error"]["type"]))
                return IRCResponse(ResponseType.Say, "I got an error code when trying to send that, sorry!", message.ReplyTo)
