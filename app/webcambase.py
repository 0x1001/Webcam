class WebcamBase(object):
    def record_motion(self):
        while not self._exit():
            self._motion_start_detection()
            if self._motion_wait():
                recording = self._motion_record()
                self._save_recording(recording)

    def stream(self):
        while not self._exit():
            photo = self._take_photo()
            self._save_stream(photo)
            self._wait(10)

    def clean(self):
        while not self._exit():
            self._delete_oldest()
            self._wait(600)

    def config(self):
        while not self._exit():
            if self._config_changed():
                self._config_load()
            self._wait(2)

    def close(self):
        self._exit_request()