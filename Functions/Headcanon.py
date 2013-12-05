import random
import re
import urllib2
import json
import sqlite3
from pastebin_python import PastebinPython
from pastebin_python.pastebin_exceptions import *
from pastebin_python.pastebin_constants import *
from pastebin_python.pastebin_formats import *
from string import find
from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import GlobalVars

class Instantiate(Function):
	pbin = PastebinPython(api_dev_key='cef9f4fcc03a220f47fcef895abe4cc1')
	subCommands = ["add", "search", "list", "remove", "help"]
	Help = "headcanon [function] -- used to store Symphony's headcanon!"
	Help += "\nHeadcanon functions: {}".format(", ".join(subCommands))
	Help += "\nSyntax is: "
	Help += GlobalVars.CommandChar
	Help += "headcanon help <command>"
	
	def GetResponse(self, message):
		if message.Type == "PRIVMSG" and message.Command == "headcanon":
			filename = "data/data.db"
			headcanon = []
			with sqlite3.connect(filename) as conn:
                                c = conn.cursor()
                                for row in c.execute("SELECT * FROM headcanon"):
                                        headcanon.append(row[0])
		
			if len(message.ParameterList) == 0:
				return IRCResponse(ResponseType.Say, self.Help, message.ReplyTo)
			
			subCommand = message.ParameterList[0]
			if subCommand.lower() == "help":
				try:
					helpCmd = message.ParameterList[1]
					if helpCmd not in subCommands:
						returnString = "Headcanon functions: {}".format(", ".join(subCommands))
						returnString += "\nSyntax is: "
						returnString += GlobalVars.CommandChar
						returnString += "headcanon help <command>"
					elif helpCmd == "add":
						returnString = GlobalVars.CommandChar + "headcanon add <string> - used to add lines to headcanon."
					elif helpCmd == "search":
						returnString = GlobalVars.CommandChar + "headcanon search <string> - used to search within the headcanon."
					elif helpCmd == "list":
						returnString = GlobalVars.CommandChar + "headcanon list - posts a list of all headcanon entires to pastebin"
					elif helpCmd == "remove":
						returnString = GlobalVars.CommandChar + "headcanon remove <string> - used to remove lines to the headcanon."
				except:
					returnString = "Headcanon functions: {}".format(", ".join(subCommands))
					returnString += "\nSyntax is: "
					returnString += GlobalVars.CommandChar
					returnString += "headcanon help <command>"
				return IRCResponse(ResponseType.Say, returnString, message.ReplyTo)
			
			elif subCommand.lower() == "add" and message.User.Name in GlobalVars.Admins:
				if len(message.ParameterList) == 1:
					return IRCResponse(ResponseType.Say, "Maybe you should read the help text?", message.ReplyTo)
				addString = ""
				for word in message.ParameterList[1:]:
					addString = addString + word + " "
				headcanon.append(addString)
				with sqlite3.connect(filename) as conn:
                                        c = conn.cursor
                                        c.execute("INSERT INTO headcanon VALUES (?)", addString)
				return IRCResponse(ResponseType.Say, "Successfully added line!", message.ReplyTo)
				
			elif subCommand.lower() == "search":
				returnString = "Search term not found in database!"
				try:
					hc = headcanon
					random.shuffle(hc)
					re_string = "{}".format(" ".join(message.ParameterList[1:]))
					for canon in hc:
						match = re.search(re_string, canon, re.IGNORECASE)
						if match:
							returnString = match.string
							break
					return IRCResponse(ResponseType.Say, returnString, message.ReplyTo)
				except:
					return IRCResponse(ResponseType.Say, returnString, message.ReplyTo)
				
			elif subCommand.lower() == "list":
				pasteBinString = ""
				if len(headcanon) == 0:
					return IRCResponse(ResponseType.Say, "The database is empty! D:", message.ReplyTo)
				else:
					for item in headcanon:
						pasteBinString = pasteBinString + item + "\n"
					try:
						pbin.createAPIUserKey("HubbeKing", "hgllabf2142")
						pasteBinStr = pbin.createPaste(pasteBinString, "headcanon", "text", 1, "10M")
						pasteBinUrl = self.ShortenGoogl(pasteBinStr)
						return IRCResponse(ResponseType.Say, "Link posted! (Expires in 10 minutes) " + pasteBinUrl, message.ReplyTo)
					except:
						return IRCResponse(ResponseType.Say, "Uh-oh, something broke!", message.ReplyTo)
						
			elif subCommand.lower() == "remove" and message.User.Name in GlobalVars.Admins:
				try:
					re_string = "{}".format(" ".join(message.ParameterList[1:]))
					for canon in headcanon:
						match = re.search(re_string, canon, re.IGNORECASE)
						if match:
							headcanon.remove(match.string)
							with sqlite3.connect(filename) as conn:
                                                                c = conn.cursor
                                                                c.execute("DELETE FROM headcanon WHERE canon=?", match.string)
							return IRCResponse(ResponseType.Say, 'Removed "' + match.string + '"', message.ReplyTo)
					return IRCResponse(ResponseType.Say, '"' + match.string + '"was not found!', message.ReplyTo)
				except:
					return IRCReponse(ResponseType.Say, "Something broke!", message.ReplyTo)
				
	def ShortenGoogl(url):
		post = '{{longUrl": "{0}"}}'.format(url)
		
		googlKey = 'AIzaSyCU7yKR6eTkme1cTUqFoSJxhG-v83trPy4'
		
		apiURL = 'https://www.googleapis.com/urlshortener/v1/url?key={0}'.format(googlKey)
		
		headers = {"Content-Type": "application/json"}
		
		try:
			request = urllib2.Request(apiURL, post, headers)
			response = json.loads(urllib2.urlopen(request).read())
			return response['id']
			
		except Exception, e:
			print "Goo.gl error: %s" % e
