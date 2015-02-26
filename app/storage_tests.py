import unittest


class Test_Storage(unittest.TestCase):
    def _prep_recording(self):
        import recording

        with open("test_data/test.h264", "rb") as fp:
            s = fp.read()

        return recording.Recording(s, 2)

    def _create_env(self):
        from os.path import join, dirname, abspath
        import sys

        sys.path.append(join(dirname(dirname(abspath(__file__))), "web"))

    def test_basic(self):
        import storage

        storage.Storage()

    def test_save_recording(self):
        import storage

        self._create_env()
        r = self._prep_recording()

        class TStorage(storage.Storage):
            def _add_recording_to_database(self, *args):
                pass

        s = TStorage()
        s.save_recording(r)

    def test_save_stream(self):
        import storage

        s = storage.Storage()
        s.save_stream("dummy")

if __name__ == "__main__":
    unittest.main()