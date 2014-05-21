from collections import OrderedDict
from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType
import datetime


class Module(ModuleInterface):
    triggers = ["uptime"]
    help = "uptime -- returns the uptime for the bot"

    def onTrigger(self, Hubbot, message):
        now = datetime.datetime.now()
        timeDelta = now - Hubbot.startTime
        return IRCResponse(ResponseType.Say, "I have been running for {}!".format(self.deltaTimeToString(timeDelta)), message.ReplyTo)

    def deltaTimeToString(self, timeDelta):
        """
        @type timeDelta: timedelta
        """
        d = OrderedDict()
        d['days'] = timeDelta.days
        d['hours'], rem = divmod(timeDelta.seconds, 3600)
        d['minutes'], d['seconds'] = divmod(rem, 60)  # replace _ with d['seconds'] to get seconds

        def lex(durationWord, duration):
            if duration == 1:
                return '{0} {1}'.format(duration, durationWord[:-1])
            else:
                return '{0} {1}'.format(duration, durationWord)

        deltaString = ' '.join([lex(word, number) for word, number in d.iteritems() if number > 0])
        return deltaString if len(deltaString) > 0 else 'seconds'
