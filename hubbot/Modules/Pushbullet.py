import re
import sqlite3
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel
from hubbot.response import IRCResponse, ResponseType
from pushbullet import PushBullet, InvalidKeyError


class Pushbullet(ModuleInterface):
    triggers = ["pb"]
    accessLevel = ModuleAccessLevel.ADMINS
    help = "pb [device] <text> -- Sends a pushbullet notification to the bot owner, device specification is optional."

    def getAPIkey(self):
        apiKey = None
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT apikey FROM keys WHERE name=\"pushbullet\""):
                apiKey = row[0]
        return apiKey

    def getDeviceByName(self, deviceName):
        """
        Tries to find the named devices in the list of devices availible with the current PushBullet object
        Returns the Device object if one can be found, otherwise returns None
        """
        for device in self.pb.devices:
            if device.nickname.lower() == deviceName.lower():
                return device
        return None

    def findDeviceName(self, pushMessage):
        """
        Trawls through the message, trying to figure out if a device name was given, and what it was.
        If no device name can be found, returns empty string as device name and the original message.
        If a valid device name can be found, returns the device name and the message with it stripped out as a tuple.
        """
        deviceList = []
        for device in self.pb.devices:
            deviceList.append(device.nickname)

        matchObject = re.match("(%s) (.*)" % "|".join(deviceList), pushMessage, flags=re.IGNORECASE)
        if matchObject is not None:
            return matchObject.groups()
        else:
            return "", pushMessage

    def onEnable(self):
        """
        When the module is enabled, try to get the API key for Pushbullet and authenticate with it.
        """
        try:
            self.APIKey = self.getAPIkey()
            self.pb = None
            if self.APIKey is not None:
                self.bot.logger.info("Successfully authenticated with Pushbullet API key.")
            else:
                self.bot.logger.error("Could not find Pushbullet API key!")
        except:
            self.bot.logger.error("Error when fetching Pushbullet API key!")
            raise

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        try:
            self.pb = PushBullet(self.APIKey)
            pushMessage = " ".join(message.ParameterList)
            deviceName, pushMessage = self.findDeviceName(pushMessage)
            device = self.getDeviceByName(deviceName)
            if device is not None:
                push = device.push_note("{} <{}>".format(str(message.ReplyTo), str(message.User.Name)), pushMessage)
            elif "://" in message.ParameterList[0]:
                push = self.pb.push_link("{} <{}>".format(str(message.ReplyTo), str(message.User.Name)), pushMessage)
            else:
                push = self.pb.push_note("{} <{}>".format(str(message.ReplyTo), str(message.User.Name)), pushMessage)
        except:
            self.bot.logger.exception("Pushbullet push failed!")
            return IRCResponse(ResponseType.Say, "I think something broke, I couldn't send that pushbullet.", message.ReplyTo)
        else:
            if "error" not in push:
                return IRCResponse(ResponseType.Say, "Okay, I'll send that to my owner!", message.ReplyTo)
            else:
                self.bot.logger.error("Pushbullet returned error '{}'".format(push["error"]["type"]))
                return IRCResponse(ResponseType.Say, "I got an error code when trying to send that, sorry!", message.ReplyTo)
