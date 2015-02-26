import unittest


class Test_benchmark(unittest.TestCase):
    def test_recording_save_time(self):
        import camera
        import storage
        import datetime

        cam = camera.Camera()
        cam.recording_start()
        cam.recording_wait(60)
        recording = cam.recording_stop()

        self._create_env()

        class TStorage(storage.Storage):
            def _add_recording_to_database(self, *args):
                start = datetime.datetime.now()
                super(TStorage, self)._add_recording_to_database(*args)
                stop = datetime.datetime.now()
                self._ca = (stop - start).total_seconds()

            def _convert(self, *args):
                start = datetime.datetime.now()
                super(TStorage, self)._convert(*args)
                stop = datetime.datetime.now()
                self._ct = (stop - start).total_seconds()

            def _save(self, *args):
                start = datetime.datetime.now()
                super(TStorage, self)._save(*args)
                stop = datetime.datetime.now()
                self._st = (stop - start).total_seconds()

        s = TStorage()

        s.save_recording(recording)

        print s._ct
        print s._st
        print s._ca

    def _create_env(self):
        from os.path import join, dirname, abspath
        import sys

        sys.path.append(join(dirname(dirname(abspath(__file__))), "web"))

if __name__ == "__main__":
    unittest.main()