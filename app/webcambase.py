class WebcamBase(object):
    def record_motion(self):
        while not self._exit():
            self._start_motion_detection()
            if self._wait_for_motion():
                photo = self._take_photo()
                recording = self._record_motion()
                self._save_motion(recording, photo)

    def stream(self):
        self._start_stream_server()

    def clean(self):
        while not self._exit():
            self._delete_oldest_movements()
            self._wait(600)

    def config(self):
        while not self._exit():
            if self._config_changed():
                self._config_load()
            self._wait(2)

    def close(self):
        self._exit_request()