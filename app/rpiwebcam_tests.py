import unittest


class Test_RPiWebcam(unittest.TestCase):
    def test_basic(self):
        import rpiwebcam
        import threading
        import time

        cam = rpiwebcam.RPiWebcam()
        thread = threading.Thread(target=cam.record_motion)
        thread.start()
        time.sleep(1)
        cam.close()
        thread.join()

if __name__ == "__main__":
    unittest.main()