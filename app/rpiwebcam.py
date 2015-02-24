import webcambase

_WAIT_TIME = 0.2
_MAX_RECORD_TIME = 30
_MAX_RECORDINGS_COUNT = 30


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

    def _wait(self, time=_WAIT_TIME):
        self._exit_event.wait(time)

    def _recording_start(self):
        return self._camera.recording_start()

    def _recording_stop(self):
        self._camera.recording_stop()

    def _recording_wait(self):
        import datetime

        start = datetime.datetime.utcnow()
        while True:
            self._camera.recording_wait()
            stop = datetime.datetime.utcnow()

            too_long = (stop - start).total_seconds() > _MAX_RECORD_TIME
            if too_long or self._exit():
                break

    def _take_photo(self):
        return self._camera.photo_capture()

    def _save_stream(self, photo):
        self._storage.save_stream(photo)

    def _save_recording(self, recording):
        self._storage.save_recording(recording)

    def _delete_oldest(self):
        recordings = self._storage.get_all_recordings()
        for r in recordings[_MAX_RECORDINGS_COUNT:]:
            self._storage.delete_recording(r.name)

    def _exit(self):
        return self._exit_event.is_set()

    def _exit_request(self):
        self._exit_event.set()