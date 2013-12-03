from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import GlobalVars

import string
import pickle
import re

class Instantiate(Function):
	Help = "hugs [nick] -- How many hugs has this person given and received?"
	
	def GetResponse(self, message):
		if message.Type == "ACTION":
			filename = "hugs/hugs.pkl"
			pkl_file = open(filename, "rb")
			hug_dict = pickle.load(pkl_file)
			pkl_file.close()
			commonWords = ["and","of","all","to","the","both","back","again","any","one","<3","with","","<3s","so","hard","right","in","him","her"]
			pattern = "hu+g|cuddle|snu+ggle|snu+g|squeeze|glomp"
			match = re.search(pattern, message.MessageList[0] , re.IGNORECASE)
			if match:
				receivers = []
				for nick in message.MessageList[1:]:
					if string.lower(nick) not in commonWords:
						nick = string.rstrip(nick, "\x01")
						nick = string.rstrip(nick, ".")
						nick = string.rstrip(nick, "!")
						nick = string.rstrip(nick, ",")
						nick = string.lower(nick)
						receivers.append(nick)
				for index in range(0, len(receivers)):
					giver = string.lower(message.User.Name)
					receiver = receivers[index]
					if giver not in hug_dict:
						hug_dict[giver] = [1,0]
					else:
						hug_dict[giver] = list(hug_dict[giver])
						hug_dict[giver][0] += 1
					if receiver not in hug_dict:
						hug_dict[receiver] = [0,1]
					else:
						hug_dict[receiver] = list(hug_dict[receiver])
						hug_dict[receiver][1] += 1
				output = open(filename, "wb")
				pickle.dump(hug_dict, output)
				output.close()
			
		elif message.Type == "PRIVMSG":
			if message.Command == "hugs":
				filename = "hugs/hugs.pkl"
				pkl_file = open(filename, "rb")
				hug_dict = pickle.load(pkl_file)
				pkl_file.close()
				if len(message.ParameterList) == 0:
					target = message.User.Name
				else:
					target = message.ParameterList[0]
					
				hugData = [0,0]
				matches = []
				for (user, hugCounts) in hug_dict.items():
					try:
						match = re.search(target, user, re.IGNORECASE)
					except:
						match = False
					if match:
						matches.append(match.string)
						hugData[0] += hugCounts[0]
						hugData[1] += hugCounts[1]
						
				HugString = target + " has received " + str(hugData[1]) + " hugs and given " + str(hugData[0]) + " hugs."
				matchedNicksString = "Matches found: "
				numberOfMatches = 0
				for name in matches:
					if (numberOfMatches > 9):
						matchedNicksString += "..."
						break
					elif (matches.index(name) == len(matches)-1):
						matchedNicksString += name
						numberOfMatches += 1
					else:
						matchedNicksString = matchedNicksString + name + ", "
						numberOfMatches += 1
				returnString = matchedNicksString + "\n" + HugString
				return IRCResponse(ResponseType.Say, returnString, message.ReplyTo)