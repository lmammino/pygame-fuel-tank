import time


class Time:
    def __init__(self):
        self._t0 = time.monotonic()
        self._last = time.monotonic()

    def delta_seconds(self):
        now = time.monotonic()
        ret = now - self._last
        self._last = now
        return ret

    def elapsed_seconds(self):
        return time.monotonic() - self._t0
