import webcambase

_WAIT_TIME = 0.2
_MAX_RECORD_TIME = 30


class RPiWebcam(webcambase.WebcamBase):
    def __init__(self):
        import threading
        import camera
        import storage

        self._camera = camera.Camera()
        self._storage = storage.Storage()
        self._exit_event = threading.Event()

        super(RPiWebcam, self).__init__()

    def _motion_start_detection(self):
        self._camera.motion_start_detection()

    def _motion_wait(self):
        return self._camera.motion_wait(self._exit_event)

    def _motion_record(self):
        return self._camera.motion_record(self._exit_event)

    def _wait(self):
        self._exit_event.wait(_WAIT_TIME)

    def _start_recording(self):
        return self._camera.start_recording()

    def _stop_recording(self):
        self._camera.stop_recording()

    def _wait_recording(self):
        import datetime

        start = datetime.datetime.utcnow()
        while True:
            self._camera.wait_recording()
            stop = datetime.datetime.utcnow()

            too_long = (stop - start).total_seconds() > _MAX_RECORD_TIME
            if too_long or self._exit() or not self._motion_detected():
                break

    def _save_recording(self, recording):
        self._storage.save_recording(recording)

    def _exit(self):
        return self._exit_event.is_set()

    def _exit_request(self):
        self._exit_event.set()