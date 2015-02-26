_RESOLUTION = (1280, 720)
_MOTION_RECORDING_TIME = 20
_FRAMERATE = 30


class CameraException(Exception):
    pass


class Camera(object):
    def __init__(self):
        import picamera
        import motion

        self._camera = picamera.PiCamera(framerate=_FRAMERATE, resolution=_RESOLUTION)
        self._camera.led = False

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

    def motion_start_detection(self):
        self._camera.start_recording(self._motion_recording,
                                     format='h264',
                                     splitter_port=self._motion_channel,
                                     motion_output=self._motion_detector)

        self._camera.wait_recording(1, splitter_port=self._motion_channel)

    def motion_wait(self, exit_event):
        import orevent

        self._motion_detector.reset()
        ore = orevent.OrEvent(exit_event, self._motion_detector.event())
        ore.wait()
        ore.close()
        return not exit_event.is_set()

    def motion_record(self, exit_event):
        import recording

        record_time = _MOTION_RECORDING_TIME - _MOTION_RECORDING_TIME / 4
        delta = 1

        self._led_on(motion_recording=True)
        while record_time > 0 and not exit_event.is_set():
            self._camera.wait_recording(delta, splitter_port=self._motion_channel)
            record_time -= delta

        self._camera.stop_recording(splitter_port=self._motion_channel)
        self._led_off(motion_recording=True)

        stream, recording_time = self._process_motion_recording(self._motion_recording)
        rec = recording.Recording(stream, recording_time)

        if recording_time > _MOTION_RECORDING_TIME:
            rec.cut(recording_time - _MOTION_RECORDING_TIME, recording_time)

        return rec

    def recording_start(self):
        import io

        self._led_on(recording=True)
        self._recording = io.BytesIO()
        self._camera.start_recording(self._recording,
                                     format='h264',
                                     splitter_port=self._recording_channel)

    def recording_wait(self, time=5):
        self._camera.wait_recording(time, splitter_port=self._recording_channel)

    def recording_stop(self):
        self._camera.stop_recording(splitter_port=self._recording_channel)
        self._led_off(recording=True)
        self._recording.seek(0)

        return self._recording.read()

    def photo_capture(self):
        import io

        stream = io.BytesIO()
        self._camera.capture(stream,
                             format='jpeg',
                             use_video_port=True,
                             splitter_port=self._photo_channel)

        stream.seek(0)
        return stream.read()

    def _process_motion_recording(self, stream):
        import picamera

        f_count = 0
        first_sps_header = None
        for frame in stream.frames:
            f_count += 1
            if first_sps_header is None and frame.frame_type == picamera.PiVideoFrameType.sps_header:
                first_sps_header = frame.position

        recording_time = f_count / _FRAMERATE
        stream.seek(first_sps_header)
        return stream.read(), recording_time

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

    def __del__(self):
        self._camera.close()
