from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType
import GlobalVars
import re
import subprocess


class Module(ModuleInterface):
    triggers = ["update"]
    help = "update - pulls the latest code from GitHub"

    def onTrigger(self, Hubbot, message):
        if message.User.Name not in GlobalVars.admins:
            return IRCResponse(ResponseType.Say, "Only my admins can update me!", message.ReplyTo)

        subprocess.call(["git", "fetch"])

        output = subprocess.check_output(["git", "whatchanged", "..origin/master"])
        changes = re.findall('\n\n\s{4}(.+?)\n\n', output)

        if len(changes) == 0:
            return IRCResponse(ResponseType.Say, "The bot is already up to date.", message.ReplyTo)

        changes = list(reversed(changes))
        response = "New Commits: {}".format(" | ".join(changes))

        subprocess.call(["git", "pull"])

        return IRCResponse(ResponseType.Say, response, message.ReplyTo)