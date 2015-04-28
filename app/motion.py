import picamera.array

_MIN_SAMPLES = 3  # min samples with motion. Range: 0% - 100%


class Motion(picamera.array.PiMotionAnalysis):
    def __init__(self, *args, **kwargs):
        import threading

        super(Motion, self).__init__(*args, **kwargs)

        self._event = threading.Event()
        self._last = None
        self._min_samples = None

    def analyse(self, a):
        import numpy as np

        r = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 1)

        if self._min_samples is None:
            # Ex: 81 x 40 (for recording resolution 1280 x 720) x min samples in percent
            self._min_samples = len(r) * len(r[0]) * _MIN_SAMPLES * 0.01

        if self._last is not None:
            diff = np.subtract(self._last, r)
            print (diff == 1).sum()
            if (diff == 1).sum() > self._min_samples or (diff == -1).sum() > self._min_samples:
                self._event.set()

        self._last = r

    def event(self):
        return self._event

    def reset(self):
        self._event.clear()