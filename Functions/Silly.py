from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import GlobalVars

class Instantiate(Function):
	Help = "nope, donotwant, yes, yup, store, goat, stupid, fixyou, heya, HNGH, PS, whoa, what, mybrand, both, no -- Used to post silly things!"
	
	def GetResponse(self, message):
		if message.Type != "PRIVMSG":
			return

		if message.Command.lower() == "nope":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=gvdf5n-zI14", message.ReplyTo)
			
		elif message.Command.lower() == "donotwant":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=oKI-tD0L18A", message.ReplyTo)
			
		elif message.Command.lower() == "yes":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=P3ALwKeSEYs", message.ReplyTo)
			
		elif message.Command.lower() == "store":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=iRZ2Sh5-XuM", message.ReplyTo)
			
		elif message.Command.lower() == "stupid":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=yytbDZrw1jc", message.ReplyTo)
		
		elif message.Command.lower() == "fixyou":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=oin0KNElSG0", message.ReplyTo)
		
		elif message.Command.lower() == "yup":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=K0QHw7iy1Rg", message.ReplyTo)
		
		elif message.Command.lower() == "heya":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=ZZ5LpwO-An4", message.ReplyTo)
		
		elif message.Command.lower() == "what":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=PDXrXBsTFSE", message.ReplyTo)
		
		elif message.Command.lower() == "goat":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=SIaFtAKnqBU", message.ReplyTo)
		
		elif message.Command.lower() == "mybrand":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=V-fRuoMIfpw", message.ReplyTo)
			
		elif message.Command.lower() == "whoa":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=6q-gHrEaEAs", message.ReplyTo)
		
		elif message.Command.lower() == "hngh":
			return IRCResponse(ResponseType.Say, "http://24.media.tumblr.com/tumblr_malzltlKk21rggqwfo1_500.gif", message.ReplyTo)
		
		elif message.Command.lower() == "ps" or message.Command.lower() == "psc":
			return IRCResponse(ResponseType.Say, "https://docs.google.com/document/d/1C4Maba3fXrLYMMIXK67OOn7C2c31V6nff5inGAZStsw/edit?pli=1", message.ReplyTo)
		
		elif message.Command.lower() == "both":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=OawrlVoQqSs", message.ReplyTo)
		
		elif message.Command.lower() == "no":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=YKss2uYpih8", message.ReplyTo)
			