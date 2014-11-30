from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType
import urllib, json, random


class Youtube(ModuleInterface):
    triggers = ["randomyt", "latestyt"]
    help = "randomyt/latestyt [channel] -- gets random/latest youtube video from the specified channel."

    def onTrigger(self, message):
        """
        @type message: IRCMessage.IRCMessage
        """
        if message.Command == "randomyt":
            if len(message.ParameterList) == 0:
                return IRCResponse(ResponseType.Say, "You didn't specify a channel!", message.ReplyTo)
            try:
                author = " ".join(message.ParameterList)
                feed = urllib.urlopen(r'https://gdata.youtube.com/feeds/api/users/{}?alt=json&v=2'.format(author))
                numberOfVids = json.load(feed)
                listOfDicts = numberOfVids['entry']['gd$feedLink']
                for dict in listOfDicts:
                    if dict['rel'] == "http://gdata.youtube.com/schemas/2007#user.uploads":
                        numberOfVids = dict["countHint"]
                randomVid = random.randrange(1,numberOfVids)
                inp = urllib.urlopen(r'http://gdata.youtube.com/feeds/api/videos?alt=json&start-index={}&max-results=1&author={}'.format(randomVid,author))
                resp = json.load(inp)
                inp.close()
                returnVid = random.choice(resp['feed']['entry'])
                return IRCResponse(ResponseType.Say, "{} -- {}".format(returnVid['title']['$t'].encode("utf-8","ignore"), returnVid['link'][0]['href'].split("&",1)[0]), message.ReplyTo)
            except Exception, ex:
                print ex.args
                return IRCResponse(ResponseType.Say, "Something broke.", message.ReplyTo)
        if message.Command == "latestyt":
            if len(message.ParameterList) == 0:
                return IRCResponse(ResponseType.Say, "You didn't specify a channel!", message.ReplyTo)
            try:
                author = " ".join(message.ParameterList)
                inp = urllib.urlopen(r'http://gdata.youtube.com/feeds/api/videos?alt=json&orderby=published&author=' + author)
                resp = json.load(inp)
                inp.close()
                returnVid = resp['feed']['entry'][0]
                return IRCResponse(ResponseType.Say, "{} -- {}".format(returnVid['title']['$t'].encode("utf-8","ignore"), returnVid['link'][0]['href'].split("&",1)[0]), message.ReplyTo)
            except Exception, ex:
                print ex.args
                return IRCResponse(ResponseType.Say, "Yeah no. That ain't happening.", message.ReplyTo)
