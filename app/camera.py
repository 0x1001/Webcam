_RESOLUTION = (1280, 720)
_MOTION_RECORDING_TIME = 20


class Camera(object):
    def __init__(self):
        import picamera
        import motion

        self._camera = picamera.PiCamera()
        self._camera.resolution = _RESOLUTION
        self._camera.led = False

        self._motion_recording = None
        self._motion_detector = motion.Motion(self._camera)
        self._motion_channel = 1
        self._motion_recording_flag = False

        self._recording = None
        self._recording_channel = 0
        self._recording_flag = False

        self._photo_channel = 2

    def motion_start_detection(self):
        import picamera

        self._motion_recording = picamera.PiCameraCircularIO(self._camera, seconds=_MOTION_RECORDING_TIME)
        self._camera.start_recording(self._motion_recording,
                                     format='h264',
                                     splitter_port=self._motion_channel,
                                     motion_output=self._motion_detector)

    def motion_wait(self, exit_event):
        import orevent

        self._motion_detector.reset()
        ore = orevent.OrEvent(exit_event, self._motion_detector.event())
        ore.wait()
        ore.close()
        return not exit_event.is_set()

    def motion_record(self, exit_event):
        record_time = _MOTION_RECORDING_TIME - 5
        delta = 1

        self._led_on(motion_recording=True)
        while record_time > 0 and not exit_event.is_set():
            self._camera.wait_recording(delta, splitter_port=self._motion_channel)
            record_time -= delta

        self._camera.stop_recording(splitter_port=self._motion_channel)
        self._led_off(motion_recording=True)

        return self._process_motion_recording(self._motion_recording)

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

        return self._recording

    def photo_capture(self):
        import io

        stream = io.BytesIO()
        self._camera.capture(stream,
                             format='jpeg',
                             use_video_port=True,
                             splitter_port=self._photo_channel)

        stream.seek(0)
        return stream.getvalue()

    def _process_motion_recording(self, stream):
        import picamera

        for frame in stream.frames:
            if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break

        return stream.read()

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
