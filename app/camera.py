_RESOLUTION = (1280, 720)
_MOTION_RECORDING_TIME = 20
_FRAMERATE = 30
_ROTATE = 270


class CameraException(Exception):
    pass


class Camera(object):
    def __init__(self):
        import threading
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

        self._recording = None
        self._recording_channel = 0
        self._recording_flag = False

        self._photo_channel = 2
        self._photo_latest = None
        self._photo_camera = threading.Thread(target=self._photo_camera_thread)

        self._exit = threading.Event()

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
        import orevent

        ore = orevent.OrEvent(exit_event, self._motion_detector.event())
        ore.wait()
        ore.close()
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

    def start_recording(self):
        import io

        self._led_on(recording=True)
        self._recording = io.BytesIO()
        self._camera.start_recording(self._recording,
                                     format='h264',
                                     splitter_port=self._recording_channel)

    def wait_for_recording(self, time=5):
        self._camera.wait_recording(time, splitter_port=self._recording_channel)

    def stop_recording(self):
        self._camera.stop_recording(splitter_port=self._recording_channel)
        self._led_off(recording=True)
        self._recording.seek(0)

        return self._recording.read()

    def take_photo(self):
        import photo
        return photo.Photo(self._photo_latest)

    def close(self):
        self._exit.set()
        self._camera.close()
        if self._photo_camera.is_alive():
            self._photo_camera.join()

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

        while not self._exit.wait(0.2):
            stream = io.BytesIO()
            self._camera.capture(stream,
                                 format='jpeg',
                                 use_video_port=True,
                                 splitter_port=self._photo_channel)

            stream.seek(0)
            self._photo_latest = stream.read()

    def _led_on(self, recording=False, motion_recording=False):
        if recording or motion_recording:
            self._camera.led = True

        if recording:
            self._recording_flag = True

        if motion_recording:
            self._motion_recording_flag = True

    def _led_off(self, recording=False, motion_recording=False):
        if recording:
            self._recording_flag = False

        if motion_recording:
            self._motion_recording_flag = False

        if not self._recording_flag and not self._motion_recording_flag:
            self._camera.led = False
