import unittest


class Test_Camera(unittest.TestCase):

    def test_stop_start(self):
        import camera
        camera.Camera()

    def test_record(self):
        import time
        import camera

        cam = camera.Camera()
        cam.recording_start()
        time.sleep(0.5)
        cam.recording_stop()

    def test_capture(self):
        import camera
        import time

        cam = camera.Camera()
        cam.recording_start()
        time.sleep(0.5)
        cam.photo_capture()
        time.sleep(0.5)
        cam.recording_stop()

    def test_motion_detection(self):
        import camera
        import threading

        e = threading.Event()
        e.set()

        cam = camera.Camera()
        cam.motion_start_detection()
        cam.motion_wait(e)

    def test_motion_recording(self):
        import camera
        import threading

        e = threading.Event()
        e.set()

        cam = camera.Camera()
        cam.motion_start_detection()
        cam.motion_wait(e)
        cam.motion_record(e)

if __name__ == "__main__":
    unittest.main()