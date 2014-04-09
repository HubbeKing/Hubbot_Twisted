import datetime
from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import GlobalVars

class Instantiate(Function):
	Help = "donotwant, yes, yup, store, goat, stupid, fixyou, heya, HNGH, PS, whoa, what, mybrand, both, no, disappoint -- Used to post silly things! Usage: %s<thing>" %GlobalVars.CommandChar
        seconds = 300
        lastTriggered = datetime.datetime.min
	
	def GetResponse(self, HubbeBot, message):
		if message.Type != "PRIVMSG":
			return
		if message.Command == "silly":
                        return IRCResponse(ResponseType.Say, self.Help, message.ReplyTo)
		if message.Command == "nope":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=gvdf5n-zI14", message.ReplyTo)
			
		elif message.Command == "donotwant":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=oKI-tD0L18A", message.ReplyTo)
			
		elif message.Command == "yes":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=P3ALwKeSEYs", message.ReplyTo)
			
		elif message.Command == "store":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=iRZ2Sh5-XuM", message.ReplyTo)
			
		elif message.Command == "stupid":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=yytbDZrw1jc", message.ReplyTo)
		
		elif message.Command == "fixyou":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=oin0KNElSG0", message.ReplyTo)
		
		elif message.Command == "yup":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=K0QHw7iy1Rg", message.ReplyTo)
		
		elif message.Command == "heya":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=ZZ5LpwO-An4", message.ReplyTo)
		
		elif message.Command == "what":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=PDXrXBsTFSE", message.ReplyTo)
		
		elif message.Command == "goat":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=SIaFtAKnqBU", message.ReplyTo)
		
		elif message.Command == "mybrand":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=V-fRuoMIfpw", message.ReplyTo)
			
		elif message.Command == "whoa":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=6q-gHrEaEAs", message.ReplyTo)
		
		elif message.Command == "hngh":
			return IRCResponse(ResponseType.Say, "http://24.media.tumblr.com/tumblr_malzltlKk21rggqwfo1_500.gif", message.ReplyTo)
		
		elif message.Command == "ps" or message.Command == "psc":
			return IRCResponse(ResponseType.Say, "https://docs.google.com/document/d/1C4Maba3fXrLYMMIXK67OOn7C2c31V6nff5inGAZStsw/edit?pli=1", message.ReplyTo)
		
		elif message.Command == "both":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=OawrlVoQqSs", message.ReplyTo)
		
		elif message.Command == "no":
			return IRCResponse(ResponseType.Say, "http://www.youtube.com/watch?v=YKss2uYpih8", message.ReplyTo)
			
		elif message.Command == "hunt":
			if message.User.Name in GlobalVars.admins:
				line1 = "LAPTOP CHAT ENGAGE"
				line2 = "THRUSTERS TO MAXIMUM POWER"
				line3 = "FLOOD TUBES THREE AND FOUR"
				line4 = "HUNT FOR RED OCTOBER"
				return IRCResponse(ResponseType.Say, line1, message.ReplyTo), IRCResponse(ResponseType.Say, line2, message.ReplyTo), IRCResponse(ResponseType.Say, line3, message.ReplyTo), IRCResponse(ResponseType.Say, line4, message.ReplyTo)
			
                elif message.Command == "<thing>":
                        return IRCResponse(ResponseType.Say, "Har har.", message.ReplyTo)

                elif message.Command.startswith("disappoint"):
                        return IRCResponse(ResponseType.Say, "https://31.media.tumblr.com/cea6574a24b490ada8bec694e87b307b/tumblr_n3blu9k5CW1tsipf6o6_400.gif", message.ReplyTo)
