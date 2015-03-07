import picamera.array

_MAGNITUDE = 0  # Motion vector magnitude. Range: 0 - 255
_MIN_SAMPLES = 0.5  # min samples with motion. Range: 0% - 100%
_MAX_SAMPLES = 10  # max samples with motion. Range: 0% - 100%
_MIN_MOTION_FRAMES = 3  # How many frames have to see motion before trigger motion detected

_MIN_SAMPLES *= 0.01
_MAX_SAMPLES *= 0.01


class Motion(picamera.array.PiMotionAnalysis):
    def __init__(self, *args, **kwargs):
        import threading

        super(Motion, self).__init__(*args, **kwargs)

        self._frames_with_motion = 0
        self._event = threading.Event()

    def analyse(self, a):
        import numpy as np

        r = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)

        samples = len(r) * len(r[0])  # Size of frame. Ex: 81 x 40 for recording resolution 1280 x 720.

        samples_min = samples * _MIN_SAMPLES  # min number of samples with motion magnitue greater than _MAGNITUDE
        samples_max = samples * _MAX_SAMPLES  # max number of samples with motion magnitue greater than _MAGNITUDE

        motion_samples = (r > _MAGNITUDE).sum()  # Finds number of samples with motion magnitue greater than _MAGNITUDE

        if motion_samples > samples_min and motion_samples < samples_max:
            self._motion_frames += 1

            if self._motion_frames == _MIN_MOTION_FRAMES:  # Checks if motion was also detected on previous frames
                self._motion_frames = 0
                self._event.set()
        else:
            self._motion_frames = 0

    def event(self):
        return self._event

    def reset(self):
        self._event.clear()