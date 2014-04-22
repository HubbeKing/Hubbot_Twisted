from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import GlobalVars

import string
import sqlite3
import re

class Instantiate(Function):
	Help = "hugs [nick] -- How many hugs has this person given and received?"
	# hug_dict is : {"nick":[given, received]}
	
	def GetResponse(self, HubbeBot, message):
		if message.Type == "ACTION":
			filename = "data/data.db"
			hug_dict = {}
			with sqlite3.connect(filename) as conn:
                                c = conn.cursor()
                                for row in c.execute("SELECT * FROM hugs"):
                                        hug_dict[row[0]] = [row[1], row[2]]
			pattern = "hu+g|cuddle|snu+ggle|snu+g|squeeze|glomp"
			match = re.search(pattern, message.MessageList[0] , re.IGNORECASE)
			if match:
				receivers = []
				for nick in message.MessageList[1:]:
					if string.lower(nick) not in GlobalVars.commonWords:
						nick = string.rstrip(nick, "\x01")
						nick = string.rstrip(nick, ".")
						nick = string.rstrip(nick, "!")
						nick = string.rstrip(nick, ",")
						nick = string.lower(nick)
						regexPattern = r"^[^a-zA-Z0-9`_\[\]\{\}\|\^\\]+$"
						invalid = re.match(regexPattern, nick)
						if not invalid:
                                                        receivers.append(nick)
				for index in range(0, len(receivers)):
					giver = string.lower(message.User.Name)
					receiver = receivers[index]
					if giver not in hug_dict:
						hug_dict[giver] = [1,0]
						with sqlite3.connect(filename) as conn:
                                                        c = conn.cursor()
                                                        c.execute("INSERT INTO hugs VALUES (?,?,?)", (giver,1,0))
                                                        conn.commit()
					else:
						hug_dict[giver] = list(hug_dict[giver])
						hug_dict[giver][0] += 1
						with sqlite3.connect(filename) as conn:
                                                        c = conn.cursor()
                                                        c.execute("UPDATE hugs SET given=? WHERE nick=?", (hug_dict[giver][0], giver))
                                                        conn.commit()
					if receiver not in hug_dict:
						hug_dict[receiver] = [0,1]
						with sqlite3.connect(filename) as conn:
                                                        c = conn.cursor()
                                                        c.execute("INSERT INTO hugs VALUES (?,?,?)", (receiver,0,1))
                                                        conn.commit()
					else:
						hug_dict[receiver] = list(hug_dict[receiver])
						hug_dict[receiver][1] += 1
						with sqlite3.connect(filename) as conn:
                                                        c = conn.cursor()
                                                        c.execute("UPDATE hugs SET received=? WHERE nick=?", (hug_dict[receiver][1], receiver))
                                                        conn.commit()
			
		elif message.Type == "PRIVMSG":
			if message.Command == "hugs":
				filename = "data/data.db"
				hug_dict = {}
				with sqlite3.connect(filename) as conn:
                                        c = conn.cursor()
                                        for row in c.execute("SELECT * FROM hugs"):
                                                hug_dict[row[0]] = [row[1], row[2]]
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
						
				HugString = "{} has received {} hugs and given {} hugs.".format(target, hugData[1], hugData[0])
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
				if len(matches) > 30:
                                        matchedNicksString = "Matches found: LOTS."
				return IRCResponse(ResponseType.Say, matchedNicksString, message.ReplyTo), IRCResponse(ResponseType.Say, HugString, message.ReplyTo)
