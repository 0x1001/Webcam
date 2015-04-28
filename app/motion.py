import picamera.array

_THRESHOLD = 3
_SKIP_FRAMES = 4


class Motion(picamera.array.PiMotionAnalysis):
    def __init__(self, *args, **kwargs):
        import threading
        import Queue

        super(Motion, self).__init__(*args, **kwargs)

        self._event = threading.Event()

        self._processing_queue = Queue.Queue(1)

        self._processing_thread = threading.Thread(target=self._processing)
        self._processing_thread.setDaemon(True)
        self._processing_thread.start()

        self._skip = 0

    def event(self):
        return self._event

    def reset(self):
        self._event.clear()

    def analyse(self, a):
        import Queue

        if not self._skip_frame() and not self._event.is_set():
            try:
                self._processing_queue.put(a, block=False)
            except Queue.Full:
                pass

    def _skip_frame(self):
        if self._skip == _SKIP_FRAMES:
            self._skip = 0
            return False
        else:
            self._skip += 1
            return True

    def _processing(self):
        import numpy as np

        while True:
            a = self._processing_queue.get()

            r = np.sqrt(
                np.square(a['x'].astype(np.float)) +
                np.square(a['y'].astype(np.float))
                ).clip(0, 255)  # Magnitude: 0 to 255

            phi = (np.arctan2(
                  a['y'].astype(np.float),
                  a['x'].astype(np.float)) +
                  np.pi) * 180 / (2 * np.pi)  # Angle degree: -90 to 90.

            if self._find_motion(r, phi):
                self._event.set()

    def _find_motion(self, r, phi):
        for x in range(len(r)):
            for y in range(len(r[0])):
                if r[x][y] > _THRESHOLD:
                    if self._check_adjacent(x, y, r, phi):
                        return True

        return False

    def _check_adjacent(self, x, y, r, phi):
        mag_min = r[x][y] - 2
        mag_max = r[x][y] + 2
        ang_min = phi[x][y] - 10
        ang_max = phi[x][y] + 10
        hits = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                try:
                    r[x + i][y + j]
                    phi[x + i][y + j]
                except IndexError:
                    continue

                if mag_min < r[x + i][y + j] and r[x + i][y + j] > mag_max:
                    if ang_min < phi[x + i][y + j] and phi[x + i][y + j] > ang_max:
                        hits += 1

        return hits >= 5
