import unittest


class Test_Camera(unittest.TestCase):

    def test_stop_start(self):
        import camera

        camera.Camera()

    def test_record(self):
        import time
        import camera

        cam = camera.Camera()
        cam.start_recording()
        time.sleep(0.5)
        cam.stop_recording()

    def test_capture(self):
        import camera
        import time

        cam = camera.Camera()
        cam.start_recording()
        time.sleep(0.5)
        cam.capture_photo()
        time.sleep(0.5)
        cam.stop_recording()

if __name__ == "__main__":
    unittest.main()