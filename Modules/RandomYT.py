from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType
import urllib, json, random


class Module(ModuleInterface):
    triggers = ["randomyt"]
    help = "randomyt [channel] -- gets a random youtube video from the specified channel."

    def onTrigger(self, Hubbot, message):
        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say, "You didn't specify a channel!", message.ReplyTo)
        try:
            author = " ".join(message.ParameterList)
            inp = urllib.urlopen(r'http://gdata.youtube.com/feeds/api/videos?alt=json&orderby=published&author=' + author)
            resp = json.load(inp)
            inp.close()
            returnVid = random.choice(resp['feed']['entry'])
            return IRCResponse(ResponseType.Say, "{} -- {}".format(returnVid['title']['$t'], returnVid['link'][0]['href'].split("&",1)[0]), message.ReplyTo)
        except:
            return IRCResponse(ResponseType.Say, "Yeah no. That ain't happening.", message.ReplyTo)