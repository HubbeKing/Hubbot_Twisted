from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import GlobalVars

import re

class Instantiate(Function):
    Help = "leave/gtfo - makes the bot leave the current channel"

    def GetResponse(self, HubbeBot, message):
        if message.Type != 'PRIVMSG':
            return
        
        match = re.search('^leave|gtfo$', message.Command, re.IGNORECASE)
        if not match:
            return
            
        if message.User.Name not in GlobalVars.admins:
            return IRCResponse(ResponseType.Say, 'Only my admins can tell me to {}'.format(message.Command), message.ReplyTo)
        
        if len(message.ParameterList) > 0:
            HubbeBot.channels.remove(message.ReplyTo)
            return IRCResponse(ResponseType.Raw, 'PART {} :{}'.format(message.ReplyTo, message.Parameters), '')
        else:
            HubbeBot.channels.remove(message.ReplyTo)
            return IRCResponse(ResponseType.Raw, 'PART {} :toodles!'.format(message.ReplyTo), '')

