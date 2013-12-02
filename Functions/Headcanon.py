import random
import re
import urllib2
import json
import pickle
from pastebin_python import PastebinPython
from pastebin_python.pastebin_exceptions import *
from pastebin_python.pastebin_constants import *
from pastebin_python.pastebin_formats import *
from string import find

class Instantiate(Function):
	pbin = PastebinPython(api_dev_key='cef9f4fcc03a220f47fcef895abe4cc1')
	Help = "headcanon [add/search/list/remove/help] -- used to store Symphony's headcanon!"
	
	def GetResponse(self, message):
		if message.Type != "PRIVMSG":
			return
		