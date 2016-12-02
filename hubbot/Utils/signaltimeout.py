# https://gist.github.com/ekimekim/b01158dc36c6e2155046684511595d57
# Thank you ekimekim

import os
import signal
import subprocess


class Timeout(Exception):
    """This is raised when a timeout occurs"""

    def __init__(self):
        self.message = "The requested operation has timed out."

    def __str__(self):
        return self.message


class SignalTimeout(object):
    """
    Context manager that raises a Timeout if the inner block takes too long.
    Will even interrupt hard loops in C by raising from an OS signal.
    """
    
    def __init__(self, timeout, timeout_signal=signal.SIGUSR1, to_raise=Timeout):
        self.timeout = float(timeout)
        self.signal = timeout_signal
        self.to_raise = to_raise
        self.old_handler = None
        self.proc = None

    def __enter__(self):
        self.old_handler = signal.signal(self.signal, self._on_signal)
        self.proc = subprocess.Popen('sleep {timeout} && kill -{signal} {pid}'.format(
            timeout=self.timeout,
            signal=self.signal,
            pid=os.getpid(),
        ),
            shell=True,
        )

    def __exit__(self, *exc_info):
        if self.proc.poll() is None:
            self.proc.kill()
        my_handler = signal.signal(self.signal, self.old_handler)
        assert my_handler == self._on_signal, "someone else has been fiddling with our signal handler?"

    def _on_signal(self, signum, frame):
        if self.old_handler:
            self.old_handler(signum, frame)
        raise self.to_raise
