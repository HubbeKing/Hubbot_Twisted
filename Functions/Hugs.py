from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import GlobalVars

class Instantiate(Function):
	Help = "hugs [nick] -- How many hugs has this person given and received?"
	
	if message.Type == "ACTION":
		#track hugs
	elif message.Type == "PRIVMSG":
		if message.Command == "hugs":
			#return hug amount