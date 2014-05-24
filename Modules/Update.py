from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType
import re
import subprocess


class Update(ModuleInterface):
    triggers = ["update"]
    help = "update - pulls the latest code from GitHub"
    accessLevel = 1

    def onTrigger(self, message):
        subprocess.call(["git", "fetch"])

        output = subprocess.check_output(["git", "whatchanged", "..origin/master"])
        changes = re.findall('\n\n\s{4}(.+?)\n\n', output)

        if len(changes) == 0:
            return IRCResponse(ResponseType.Say, "The bot is already up to date.", message.ReplyTo)

        changes = list(reversed(changes))
        response = "New Commits: {}".format(" | ".join(changes))

        subprocess.call(["git", "pull"])

        return IRCResponse(ResponseType.Say, response, message.ReplyTo)