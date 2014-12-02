class IRCChannel(object):
    def __init__(self, name):
        self.Name = name
        self.Users = {}
        self.Ranks = {}
        self.NamesListComplete = True