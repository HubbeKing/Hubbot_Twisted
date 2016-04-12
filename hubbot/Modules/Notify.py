import re
import sqlite3
from hubbot.moduleinterface import ModuleInterface
from pushbullet import PushBullet, InvalidKeyError


class Notify(ModuleInterface):
    pb = None
    APIKey = None
    regexPattern = "Hubbe.*"

    def getAPIkey(self):
        """
        Get the API key for pushbullet from the sqlite database.
        """
        apiKey = None
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT apikey FROM keys WHERE name=\"pushbullet\""):
                apiKey = row[0]
        return apiKey

    def onEnable(self):
        """
        When the module is enabled, try to get the API key for Pushbullet and authenticate with it.
        """
        try:
            self.APIKey = self.getAPIkey()
            self.pb = None
            if self.APIKey is not None:
                try:
                    self.pb = PushBullet(self.APIKey)
                except InvalidKeyError:
                    self.bot.logger.exception("Pushbullet API key invalid!")
                    raise
                self.bot.logger.info("Successfully authenticated with Pushbullet API key.")
            else:
                self.bot.logger.error("Could not find Pushbullet API key!")
        except:
            self.bot.logger.error("Error when fetching Pushbullet API key!")
            raise

    def shouldTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Type in self.acceptedTypes:
            match = re.search(self.regexPattern, message.MessageString, re.IGNORECASE)
            if match:
                return True
            else:
                return False

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        try:
            self.pb.refresh()
            phone = self.getDeviceByName("phone")
            push = phone.push_note("Highlight in {}".format(message.Channel.Name), "<{}> {}".format(message.User.Name, message.MessageString))
        except:
            self.bot.logger.exception("Highlighting pushbullet push failed.")
        else:
            if "error" in push:
                self.bot.logger.error("Pushbullet returned error '{}'".format(push["error"]["type"]))

    def getDeviceByName(self, deviceName):
        """
        Tries to find the named device in the list of devices availible with the current PushBullet object.
        Returns the Device object if one can be found, otherwise returns None.
        """
        for device in self.pb.devices:
            if device.nickname.lower() == deviceName.lower():
                return device
        return None