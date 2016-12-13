from __future__ import unicode_literals
from collections import OrderedDict


# mostly taken from dave_random's UnsafeBot (whose source is not generally accessible)
def delta_time_to_string(time_delta, resolution='m'):
    """
    returns a string version of the given timedelta, with a resolution of minutes ('m') or seconds ('s')
    @type time_delta: timedelta
    @type resolution: str
    """
    d = OrderedDict()
    d['days'] = time_delta.days
    d['hours'], rem = divmod(time_delta.seconds, 3600)
    if resolution == 'm' or resolution == 's':
        d['minutes'], seconds = divmod(rem, 60)
        if resolution == 's':
            d['seconds'] = seconds

    def lex(duration_word, duration):
        if duration == 1:
            return '{0} {1}'.format(duration, duration_word[:-1])
        else:
            return '{0} {1}'.format(duration, duration_word)

    delta_string = ' '.join([lex(word, number) for word, number in d.iteritems() if number > 0])
    return delta_string if len(delta_string) > 0 else 'seconds'
