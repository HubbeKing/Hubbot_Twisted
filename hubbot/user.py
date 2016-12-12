class IRCUser(object):
    def __init__(self, user):
        self.user = None
        self.hostmask = None
        self.last_active = None

        if "!" in user:
            user_array = user.split("!")
            self.name = user_array[0]
            if len(user_array) > 1:
                user_array = user_array[1].split("@")
                self.user = user_array[0]
                self.hostmask = user_array[1]
        else:
            self.name = user
            self.user = "anon"
            self.hostmask = "unknown"

    def __str__(self):
        return "{}!{}@{}".format(self.name, self.user, self.hostmask)
