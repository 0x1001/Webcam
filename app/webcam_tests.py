import unittest


class Test_Webcam(unittest.TestCase):

    def test_basic(self):
        import webcam

        class Cam(webcam.Webcam):
            def _motion_detected(self):
                pass

            def _wait(self):
                pass

            def _start_recording(self):
                pass

            def _stop_recording(self):
                pass

            def _wait_recording(self):
                pass

            def _exit(self):
                return True

        cam = Cam()
        cam.start()


if __name__ == "__main__":
    unittest.main()