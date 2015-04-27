import webcambase

_WAIT_TIME = 0.2
_MAX_RECORD_TIME = 30
_STREAM_SIZE = 640, 360

_MAX_RECORDINGS_COUNT = 150
_MAX_PHOTOS_COUNT = 300
_MAX_MOVEMENTS_COUNT = 1000


class RPiWebcam(webcambase.WebcamBase):
    def __init__(self):
        import threading
        import camera
        import storage

        self._camera = camera.Camera()
        self._storage = storage.Storage()
        self._exit_event = threading.Event()

        self._camera.start()
        self._stream_server = None

        super(RPiWebcam, self).__init__()

    def _start_stream_server(self):
        from gevent.server import StreamServer

        def handle(socket, address):
            p = self._take_photo()
            socket.sendall(p.get_base64_contents(_STREAM_SIZE))

        self._stream_server = StreamServer(('127.0.0.1', 1234), handle)
        self._stream_server.serve_forever()

    def _start_motion_detection(self):
        self._camera.start_motion_detection()

    def _wait_for_motion(self):
        return self._camera.wait_for_motion(self._exit_event)

    def _record_motion(self):
        return self._camera.record_motion(self._exit_event)

    def _wait(self, time=_WAIT_TIME):
        self._exit_event.wait(time)

    def _start_recording(self):
        return self._camera.start_recording()

    def _stop_recording(self):
        self._camera.stop_recording()

    def _wait_for_recording(self):
        import datetime

        start = datetime.datetime.utcnow()
        while True:
            self._camera.wait_for_recording()
            stop = datetime.datetime.utcnow()

            too_long = (stop - start).total_seconds() > _MAX_RECORD_TIME
            if too_long or self._exit():
                break

    def _take_photo(self):
        return self._camera.take_photo()

    def _save_photo(self, photo):
        self._storage.save_photo(photo)

    def _save_recording(self, recording, photo):
        self._storage.save_photo(photo)
        self._storage.save_recording(recording, photo)

    def _save_motion(self, recording, photo):
        import threading

        def _do():
            self._storage.save_photo(photo)
            self._storage.save_recording(recording, photo)
            self._storage.save_motion(recording, photo)

        threading.Thread(target=_do).start()

    def _delete_oldest_recordings(self):
        recordings = self._storage.get_all_recordings()
        for r in recordings[_MAX_RECORDINGS_COUNT:]:
            self._storage.delete_recording(r.name)

    def _delete_oldest_photos(self):
        photos = self._storage.get_all_photos()
        for p in photos[_MAX_PHOTOS_COUNT:]:
            self._storage.delete_photo(p.name, p.thumbnail)

    def _delete_oldest_movements(self):
        movements = self._storage.get_all_movements()
        for m in movements[_MAX_MOVEMENTS_COUNT:]:
            self._storage.delete_movement(m.id)

    def _exit(self):
        return self._exit_event.is_set()

    def _exit_request(self):
        self._exit_event.set()

        if self._stream_server is not None:
            self._stream_server.stop()

        self._camera.close()