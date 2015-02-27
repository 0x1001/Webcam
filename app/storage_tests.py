import unittest
import storage


class Test_Storage(unittest.TestCase):
    class TStorage(storage.Storage):
        def _add_recording_to_database(self, *args):
            pass

        def _add_photo_to_database(self, *args):
            pass

        def _add_motion_to_database(self, *args):
            pass

    def _prep_recording(self):
        import recording

        with open("test_data/test.h264", "rb") as fp:
            s = fp.read()

        return recording.Recording(s, 2)

    def _prep_photo(self):
        import photo

        with open("test_data/sample1.jpg", "rb") as fp:
            s = fp.read()

        return photo.Photo(s)

    def _create_env(self):
        from os.path import join, dirname, abspath
        import sys

        sys.path.append(join(dirname(dirname(abspath(__file__))), "web"))

    def test_basic(self):
        storage.Storage()

    def test_save_recording(self):
        self._create_env()
        r = self._prep_recording()
        p = self._prep_photo()
        s = self.TStorage()

        s.save_recording(r, p)
        s.save_photo(p)
        s.save_motion(r, p)

    def test_save_stream(self):
        import storage

        s = storage.Storage()
        s.save_stream("dummy")

if __name__ == "__main__":
    unittest.main()