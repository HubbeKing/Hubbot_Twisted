import signal


class Timeout(Exception):
    """Context manager which wraps code in a timeout.
  If the timeout is exceeded, the context manager will be raised.
  Example usage:
    try:
      with Timeout(5):
        time.sleep(10)
    except Timeout:
      pass
  """

    def __init__(self, duration):
        self.duration = duration

    def _handler(self, signum, frame):
        raise self

    def __enter__(self):
        self._old_handler = signal.signal(signal.SIGALRM, self._handler)
        old_alarm = signal.alarm(self.duration)
        if old_alarm:
            raise Exception("Timeout will not behave correctly in conjunction with other code that uses signal.alarm()")

    def __exit__(self, *exc_info):
        signal.alarm(0)  # cancel any pending alarm
        my_handler = signal.signal(signal.SIGALRM, self._old_handler)
        assert my_handler == self._handler, "Wrong SIGALRM handler on __exit__, is something else messing with signal handlers?"

    def __str__(self):
        return "Exceeded timeout of {} seconds".format(self.duration)
