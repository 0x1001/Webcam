class Camera(object):
    def __init__(self):
        import picamera

        self.camera = picamera.PiCamera()
        self.camera.resolution = (1280, 720)
        self.camera.led = False

    def start_recording(self):
        import io

        stream = io.BytesIO()
        self.camera.start_recording(stream, format='h264')
        self.camera.led = True
        return stream

    def wait_recording(self):
        self.camera.wait_recording(3)

    def stop_recording(self):
        self.camera.led = False
        self.camera.stop_recording()

    def capture_photo(self):
        import io

        stream = io.BytesIO()
        self.camera.capture(stream, format='jpeg', use_video_port=True)
        stream.seek(0)
        return stream

    def __del__(self):
        self.camera.close()
