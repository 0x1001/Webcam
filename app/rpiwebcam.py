import webcam

_WAIT_TIME = 0.2
_MAX_RECORD_TIME = 30


class RPiWebcam(webcam.Webcam):
    def __init__(self):
        import threading
        import camera
        import motion

        self._camera = camera.Camera()
        self._motion = motion.Motion()
        self._exit_event = threading.Event()

        super(RPiWebcam, self).__init__()

    def _wait(self):
        self._exit_event.wait(_WAIT_TIME)

    def _start_recording(self):
        return self._camera.start_recording()

    def _stop_recording(self):
        self._camera.stop_recording()

    def _wait_recording(self):
        import datetime

        start = datetime.datetime.now()
        while not self._exit() and self._motion_detected():
            self._camera.wait_recording()
            stop = datetime.datetime.now()

            if (stop - start).total_seconds() > _MAX_RECORD_TIME:
                break

    def _motion_detected(self):
        img = self._camera.capture_photo()
        return self._motion.detect(img)

    def _save_recording(self, recording):
        print "saved"

    def _exit(self):
        return self._exit_event.set()