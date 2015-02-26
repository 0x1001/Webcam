import unittest


class Test_Recording(unittest.TestCase):
    def test_basic(self):
        import recording

        with self.assertRaises(recording.RecordingException):
            recording.Recording(None, 0)

    def test_recording(self):
        import recording

        with open("test_data/test.h264", "rb") as fp:
            s = fp.read()

        r = recording.Recording(s, 2)
        r.cut(0, 1)

        with self.assertRaises(recording.RecordingException):
            r.cut(2, 1)

        r.remove()


if __name__ == "__main__":
    unittest.main()