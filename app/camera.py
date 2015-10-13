_RESOLUTION = (1280, 720)
_MOTION_RECORDING_TIME = 20
_FRAMERATE = 30
_ROTATE = 90


class CameraException(Exception):
    pass


class Camera(object):
    def __init__(self):
        import threading

        self._exit = threading.Event()

        self._setup_camera()
        self._setup_photo()

    def _setup_camera(self):
        import picamera
        import motion

        self._camera = picamera.PiCamera(framerate=_FRAMERATE, resolution=_RESOLUTION)
        self._camera.led = False
        self._camera.rotation = _ROTATE

        self._motion_recording = None
        self._motion_channel = 1
        self._motion_recording_flag = False
        self._motion_detector = motion.Motion(self._camera)
        self._motion_recording = picamera.PiCameraCircularIO(self._camera,
                                                             splitter_port=self._motion_channel,
                                                             seconds=_MOTION_RECORDING_TIME)

    def _setup_photo(self):
        import threading

        self._photo_channel = 2
        self._photo_latest = None
        self._photo_camera = threading.Thread(target=self._photo_camera_thread)
        self._photo_lock = threading.RLock()
        self._photo_ready = threading.Event()

    def start(self):
        self._photo_camera.start()

    def start_motion_detection(self):
        self._motion_recording.seek(0)
        self._motion_recording.truncate()

        self._motion_detector.reset()

        self._camera.start_recording(self._motion_recording,
                                     format='h264',
                                     splitter_port=self._motion_channel,
                                     motion_output=self._motion_detector)

    def wait_for_motion(self, exit_event):
        motion_event = self._motion_detector.event()

        while True:
            if exit_event.wait(0.2) or motion_event.wait(0.2):
                break

        if exit_event.is_set():
            self._camera.stop_recording(splitter_port=self._motion_channel)

        return not exit_event.is_set()

    def record_motion(self, exit_event):
        record_time = _MOTION_RECORDING_TIME - _MOTION_RECORDING_TIME / 4
        delta = 1

        self._led_on(motion_recording=True)
        while record_time > 0 and not exit_event.is_set():
            self._camera.wait_recording(delta, splitter_port=self._motion_channel)
            record_time -= delta

        self._camera.stop_recording(splitter_port=self._motion_channel)
        self._led_off(motion_recording=True)

        return self._process_motion_recording(self._motion_recording)

    def take_photo(self):
        import photo

        self._photo_ready.wait()

        with self._photo_lock:
            return photo.Photo(self._photo_latest)

    def close(self):
        self._exit.set()

        if self._photo_camera.is_alive():
            self._photo_camera.join()

        self._wait_for_camera_stop()

        try:
            self._camera.close()
        except Exception:
            pass  # Ignor errors

    def _wait_for_camera_stop(self):
        import picamera
        import time

        while True:
            try:
                self._camera._check_recording_stopped()
            except picamera.exc.PiCameraRuntimeError:
                time.sleep(0.2)
                continue
            else:
                break

        time.sleep(0.2)

    def _process_motion_recording(self, stream):
        import picamera
        import recording

        f_count = 0
        first_sps_header = None
        for frame in stream.frames:
            f_count += 1
            if first_sps_header is None and frame.frame_type == picamera.PiVideoFrameType.sps_header:
                first_sps_header = frame.position

        recording_time = f_count / _FRAMERATE
        stream.seek(first_sps_header)

        rec = recording.Recording(stream.read(), recording_time)

        if recording_time > _MOTION_RECORDING_TIME:
            rec.cut(recording_time - _MOTION_RECORDING_TIME, recording_time)

        return rec

    def _photo_camera_thread(self):
        import io
        from picamera.exc import PiCameraRuntimeError

        while not self._exit.wait(0.2):
            stream = io.BytesIO()

            try:
                self._camera.capture(stream,
                                     format='jpeg',
                                     use_video_port=True,
                                     splitter_port=self._photo_channel)
            except PiCameraRuntimeError as error:
                print "Cannot capture photo for stream. Error: " + str(error)
            else:
                with self._photo_lock:
                    self._photo_latest = stream.getvalue()
            finally:
                stream.close()
                self._photo_ready.set()

    def _led_on(self, motion_recording=False):
        if motion_recording:
            self._camera.led = True
            self._motion_recording_flag = True

    def _led_off(self, motion_recording=False):
        if motion_recording:
            self._motion_recording_flag = False

        if not self._motion_recording_flag:
            self._camera.led = False
