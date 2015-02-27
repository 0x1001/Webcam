import unittest


class Test_Recording(unittest.TestCase):
    def test_basic(self):
        import recording

        with self.assertRaises(recording.RecordingException):
            recording.Recording(None, 0)

    def test_recording(self):
        import recording
        import tempfile
        import os

        with open("test_data/test.h264", "rb") as fp:
            s = fp.read()

        r = recording.Recording(s, 2)
        r.cut(0, 1)

        with self.assertRaises(recording.RecordingException):
            r.cut(2, 1)

        temp_root = os.path.join(tempfile.gettempdir(), "test_recording")
        if not os.path.isdir(temp_root):
            os.makedirs(temp_root)

        temp_path = os.path.join(temp_root, r.name)
        r.save(temp_root)
        self.assertTrue(os.path.isfile(temp_path))
        r.remove()
        self.assertFalse(os.path.isfile(temp_path))


if __name__ == "__main__":
    unittest.main()