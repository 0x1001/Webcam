import picamera.array

_MAGNITUDE = 10      # If there're more than 10 vectors with a magnitude greater
_VECTOR_COUNT = 60  # than 60, then say we've detected motion


class Motion(picamera.array.PiMotionAnalysis):
    def __init__(self, *args, **kwargs):
        import threading

        super(Motion, self).__init__(*args, **kwargs)

        self._event = threading.Event()

    def analyse(self, a):
        import numpy as np

        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)

        if (a > _VECTOR_COUNT).sum() > _MAGNITUDE:
            self._event.set()

    def event(self):
        return self._event

    def reset(self):
        self._event.clear()