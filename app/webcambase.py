class WebcamBase(object):
    def record_motion(self):
        while not self._exit():
            if self._motion_detected():
                recording = self._start_recording()
                self._wait_recording()
                self._stop_recording()
                self._save_recording(recording)
            self._wait()

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