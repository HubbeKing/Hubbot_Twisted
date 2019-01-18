

class IRCChannel(object):
    def __init__(self, name):
        self.name = name
        self.users = {}
        self.ranks = {}
        self.names_list_complete = True

    def __str__(self):
        return self.name
