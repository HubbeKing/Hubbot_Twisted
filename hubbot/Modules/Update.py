from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel
from hubbot.response import IRCResponse, ResponseType
import os
import sys
import subprocess


class Update(ModuleInterface):
    triggers = ["update"]
    help = "update - pulls the latest code from GitHub"
    accessLevel = ModuleAccessLevel.ADMINS

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        subprocess.check_call(["git", "fetch"])

        output = subprocess.check_output(['git', 'log', '--no-merges',
                                          '--pretty=format:%s', '..origin/master'])
        changes = [s.strip() for s in output.splitlines()]

        if len(changes) == 0:
            return IRCResponse(ResponseType.Say, "The bot is already up to date.", message.ReplyTo)

        changes = list(reversed(changes))
        response = "New Commits: {}".format(" | ".join(changes))

        output = subprocess.check_output(['git', 'show', '--pretty=format:', '--name-only', '..origin/master'])
        filesChanged = [s.strip() for s in output.splitlines()]

        returnCode = subprocess.check_call(['git', 'merge', 'origin/master'])

        if returnCode != 0:
            return IRCResponse(ResponseType.Say,
                               'Merge after update failed, please merge manually',
                               message.ReplyTo)

        if "requirements.txt" in filesChanged:
            pip = os.path.join(os.path.dirname(sys.executable), "pip")
            returnCode = subprocess.check_call([pip, "install", "-r", "requirements.txt"])

            if returnCode != 0:
                return IRCResponse(ResponseType.Say,
                                   'Requirements update failed, please check output manually.',
                                   message.ReplyTo)

        return IRCResponse(ResponseType.Say, response, message.ReplyTo)
