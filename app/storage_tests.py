import unittest


class Test_Storage(unittest.TestCase):
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

        class TStorage(storage.Storage):
            def _convert(self, *args):
                pass

            def _add_recording_to_database(self, *args):
                pass

        s = TStorage()
        s.save_recording("dummy")

    def test_stream_photo(self):
        import storage

        s = storage.Storage()
        s.save_stream("dummy")

if __name__ == "__main__":
    unittest.main()