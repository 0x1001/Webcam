class WebcamBase(object):
    def record_motion(self):
        while not self._exit():
            self._motion_start_detection()
            if self._motion_wait():
                recording = self._motion_record()
                self._save_recording(recording)

    def clean(self):
        while not self._exit():
            if self._full_history():
                self._delete_oldest()
            self._wait()

    def config(self):
        while not self._exit():
            if self._config_changed():
                self._config_load()
            self._wait()

    def close(self):
        self._exit_request()