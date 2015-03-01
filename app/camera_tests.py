import unittest


class Test_Camera(unittest.TestCase):

    def setUp(self):
        import camera
        self.cam = camera.Camera()

    def tearDown(self):
        self.cam.close()

    def test_record(self):
        import time

        self.cam.start_recording()
        time.sleep(0.5)
        self.cam.stop_recording()

    def test_capture(self):
        import time

        self.cam.start()
        self.cam.start_recording()
        time.sleep(0.5)
        self.cam.take_photo()
        time.sleep(0.5)
        self.cam.stop_recording()

    def test_motion_detection(self):
        import threading

        e = threading.Event()
        e.set()

        self.cam.start_motion_detection()
        self.cam.wait_for_motion(e)

    def test_motion_recording(self):
        import threading

        e = threading.Event()
        e.set()

        self.cam.start_motion_detection()
        self.cam.wait_for_motion(e)
        self.cam.record_motion(e)

    def test_recording(self):
        self.cam.start_recording()
        self.cam.wait_for_recording(0.5)
        self.cam.stop_recording()


if __name__ == "__main__":
    unittest.main()