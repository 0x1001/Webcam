import unittest


class Test_Storage(unittest.TestCase):
    def _create_env(self):
        from os import environ
        from os.path import join, dirname, abspath
        import sys
        import django

        environ['DJANGO_SETTINGS_MODULE'] = 'webcam.settings'
        sys.path.append(join(dirname(dirname(abspath(__file__))), "web"))
        django.setup()

    def test_basic(self):
        import storage

        storage.Storage()

    def test_save_recording(self):
        import storage
        import StringIO

        self._create_env()

        class TStorage(storage.Storage):
            def _convert(self, path):
                return path

        s = TStorage()
        s.save_recording(StringIO.StringIO("dummy"))


if __name__ == "__main__":
    unittest.main()