import sched
import time

class FrameRunner(object):
    def __init__(self, fps, handler, args=()):
        self._initial = None
        self._frames = 0
        self._handler = handler
	self._args = args
        self.set_fps(fps)

        self._sched = sched.scheduler(time.time, time.sleep)

    def set_handler(self, handler):
        self._handler = handler
        return self

    def set_args(self, args):
        self._args = args
        return self

    def set_fps(self, fps):
        self._fps = fps
        return self

    def _do_handler(self, abstime, handler, args):
        self._handler(*args)
        self._frames += 1

        target_seconds = float(self._frames + 1) / self._fps
        target_time = self._initial + target_seconds

        if target_time <= time.time():
            return self._do_handler(None, handler, args)

        self._sched.enterabs(target_time, 1, self._do_handler, (target_time, handler, args))

    def run(self):
        self._initial = time.time()
	self._do_handler(None, self._do_handler, self._args)
        self._sched.run()

def _example_main():
    initial = time.time()
    cfg = {"last_frame": initial}
    fps = 30

    def handler(f):
        now = time.time()
        expected = (float(f._frames + 1.0) / f._fps) + f._initial
        period_ms = (now - cfg["last_frame"]) * 1000.0
        deviation_ms = (expected - now) * 1000.0

        print("%.4fms (deviation=%.2fms)" % (period_ms, deviation_ms))
        cfg["last_frame"] = now

    f = FrameRunner(fps, handler)
    f.set_args((f,))
    f.run()


if __name__ == "__main__":
    _example_main()
