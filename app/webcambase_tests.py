import unittest


class Test_WebcamBase(unittest.TestCase):

    def test_basic(self):
        import webcambase

        class Cam(webcambase.WebcamBase):
            def _exit(self):
                return True

        cam = Cam()
        cam.record_motion()
        cam.config()
        cam.clean()


if __name__ == "__main__":
    unittest.main()