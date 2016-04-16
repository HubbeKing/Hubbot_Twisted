from collections import OrderedDict


# From this SO answer: http://stackoverflow.com/a/6043797/331047
def splitUTF8(s, n):
    """Split UTF-8 s into chunks of maximum byte length n"""
    while len(s) > n:
        k = n
        while (ord(s[k]) & 0xc0) == 0x80:
            k -= 1
        yield s[:k]
        s = s[k:]
    yield s


# mostly taken from dave_random's UnsafeBot (whose source is not generally accessible)
def deltaTimeToString(timeDelta, resolution='m'):
    """
    returns a string version of the given timedelta, with a resolution of minutes ('m') or seconds ('s')
    @type timeDelta: timedelta
    @type resolution: str
    """
    d = OrderedDict()
    d['days'] = timeDelta.days
    d['hours'], rem = divmod(timeDelta.seconds, 3600)
    if resolution == 'm' or resolution == 's':
        d['minutes'], seconds = divmod(rem, 60)
        if resolution == 's':
            d['seconds'] = seconds

    def lex(durationWord, duration):
        if duration == 1:
            return '{0} {1}'.format(duration, durationWord[:-1])
        else:
            return '{0} {1}'.format(duration, durationWord)

    deltaString = ' '.join([lex(word, number) for word, number in d.iteritems() if number > 0])
    return deltaString if len(deltaString) > 0 else 'seconds'
