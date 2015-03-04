import picamera.array

_MAGNITUDE = 10      # If there're more than 10 vectors with a magnitude greater
_VECTOR_COUNT = 60  # than 60, then say we've detected motion

_ANGLE = 10    # Motion angle differenece + or - from 90.


class Motion(picamera.array.PiMotionAnalysis):
    def __init__(self, *args, **kwargs):
        import threading

        super(Motion, self).__init__(*args, **kwargs)

        self._event = threading.Event()

    def analyse(self, a):
        import numpy as np

        r = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)

        phi = ((np.arctan2(
              a['y'].astype(np.float),
              a['x'].astype(np.float)) +
              np.pi) * 180 / (2 * np.pi)
              ).clip(0, 255).astype(np.uint8)

        if ((r > _VECTOR_COUNT).sum() > _MAGNITUDE and
            ((phi > _VECTOR_COUNT).sum() > 90 + _ANGLE or
            (phi > _VECTOR_COUNT).sum() > 90 - _ANGLE)):

            self._event.set()

    def event(self):
        return self._event

    def reset(self):
        self._event.clear()