

class IRCUser(object):
    def __init__(self, user):
        self.User = None
        self.Hostmask = None
        self.LastActive = None

        if "!" in user:
            userArray = user.split("!")
            self.Name = userArray[0]
            if len(userArray) > 1:
                userArray = userArray[1].split("@")
                self.User = userArray[0]
                self.Hostmask = userArray[1]
            self.String = "{}!{}@{}".format(self.Name, self.User, self.Hostmask)
        else:
            self.Name = user
            self.String = "{}!{}@{}".format(self.Name, "a", "b")
