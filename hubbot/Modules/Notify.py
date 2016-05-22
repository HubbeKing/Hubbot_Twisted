import datetime
import re
import sqlite3
from hubbot.moduleinterface import ModuleInterface
from pushbullet import PushBullet, InvalidKeyError
from twisted.internet import reactor


class Notify(ModuleInterface):
    pb = None
    APIKey = None
    notifyTarget = "Hubbe.*"
    help = "Notify - A module that notifies HubbeKing if he's in the channel but doesn't respond to being highlighted."

    def getAPIkey(self):
        """
        Get the API key for pushbullet from the sqlite database.
        """
        apiKey = None
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT apikey FROM keys WHERE name='pushbullet'"):
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
                self.bot.logger.debug("Successfully authenticated with Pushbullet API key.")
            else:
                self.bot.logger.error("Could not find Pushbullet API key!")
        except:
            self.bot.logger.exception("Error when fetching Pushbullet API key!")
            raise

    def shouldTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Type in self.acceptedTypes and not re.search(self.notifyTarget, message.User.Name, re.IGNORECASE):
            for user in message.Channel.Users:
                targetHere = re.search(self.notifyTarget, user, re.IGNORECASE)
                if targetHere:
                    match = re.search(self.notifyTarget, message.MessageString, re.IGNORECASE)
                    if match:
                        now = datetime.datetime.now()
                        try:
                            timeDelta = now - message.Channel.Users[user].LastActive
                        except TypeError:  # this means that LastActive is None for some reason
                            timeDelta = now - datetime.datetime.min
                            self.bot.logger.exception("TypeError in module 'Notify', LastActive is probably not datetime.")
                        if timeDelta.total_seconds() > 60:
                            return True
                        else:
                            return False
                    else:
                        return False
            return False
        return False

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        targetUser = None
        for user in message.Channel.Users:
            target = re.search(self.notifyTarget, user, re.IGNORECASE)
            if target:
                targetUser = message.Channel.Users[user]
        reactor.callLater(30, self.notify, targetUser, message)

    def notify(self, target, message):
        """
        @type target: hubbot.user.IRCUser
        @type message: hubbot.message.IRCMessage
        """
        if target is not None:
            now = datetime.datetime.now()
            if (now - target.LastActive).total_seconds() > 60:
                self.bot.logger.info("Notify - Sending highlighting push.")
                try:
                    self.pb.refresh()
                    phone = self.getDeviceByName("phone")
                    if phone is not None:
                        push = phone.push_note("Highlight in {}".format(message.Channel.Name), "<{}> {}".format(message.User.Name, message.MessageString))
                    else:
                        self.bot.logger.error("Notify - Could not find phone device for highlighting push!")
                        push = None
                except:
                    self.bot.logger.exception("Notify - Unknown error when pushing highlight.")
                else:
                    if "error" in push:
                        self.bot.logger.error("Notify - Pushbullet returned error '{}'".format(push["error"]["type"]))
            else:
                self.bot.logger.info("Notify - Target user recently active, no highlighting push sent.")

    def getDeviceByName(self, deviceName):
        """
        Tries to find the named device in the list of devices availible with the current PushBullet object.
        Returns the Device object if one can be found, otherwise returns None.
        """
        for device in self.pb.devices:
            if device.nickname.lower() == deviceName.lower():
                return device
        return None
