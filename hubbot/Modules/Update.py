from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel
from hubbot.response import IRCResponse, ResponseType
import os
import sys
import subprocess


class Update(ModuleInterface):
    triggers = ["update"]
    help = "update - pulls the latest code from GitHub"
    access_level = ModuleAccessLevel.ADMINS

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        subprocess.check_call(["git", "fetch"])

        output = subprocess.check_output(['git', 'log', '--no-merges',
                                          '--pretty=format:%s', '..origin/master'])
        changes = [s.strip() for s in output.splitlines()]

        if len(changes) == 0:
            return IRCResponse(ResponseType.SAY, "The bot is already up to date.", message.reply_to)

        changes = list(reversed(changes))
        response = "New Commits: {}".format(" | ".join(changes))

        output = subprocess.check_output(['git', 'show', '--pretty=format:', '--name-only', '..origin/master'])
        files_changed = [s.strip() for s in output.splitlines()]

        return_code = subprocess.check_call(['git', 'merge', 'origin/master'])

        if return_code != 0:
            return IRCResponse(ResponseType.SAY,
                               'Merge after update failed, please merge manually',
                               message.reply_to)

        if "requirements.txt" in files_changed:
            pip = os.path.join(os.path.dirname(sys.executable), "pip")
            return_code = subprocess.check_call([pip, "install", "--update", "-r", "requirements.txt"])

            if return_code != 0:
                return IRCResponse(ResponseType.SAY,
                                   'Requirements update failed, please check output manually.',
                                   message.reply_to)

        return IRCResponse(ResponseType.SAY, response, message.reply_to)
