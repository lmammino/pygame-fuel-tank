import time


class Time:
    def __init__(self):
        self._t0 = time.monotonic()
        self._last = time.monotonic()
        self._running = True

    def delta_seconds(self):
        now = time.monotonic()
        ret = now - self._last
        self._last = now
        return ret

    def elapsed_seconds(self):
        if self._running:
            return time.monotonic() - self._t0
        return self._time_when_stopped

    def running(self):
        return self._running

    def stop(self):
        self._running = False
        self._time_when_stopped = time.monotonic() - self._t0
