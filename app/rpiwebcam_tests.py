import unittest


class Test_RPiWebcam(unittest.TestCase):
    def test_basic(self):
        import rpiwebcam

        rpiwebcam.RPiWebcam().start()

if __name__ == "__main__":
    unittest.main()