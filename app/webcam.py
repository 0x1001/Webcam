class Webcam(object):
    def start(self):
        while not self._exit():
            if self._motion_detected():
                recording = self._start_recording()
                self._wait_recording()
                self._stop_recording()
                self._save_recording(recording)
            self._wait()
