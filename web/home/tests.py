from django.test import TestCase
from home.models import get_recordings
from home.models import remove_recording


class FunctionTests(TestCase):

    def test_get_recordings(self):
        self.assertEqual(list(get_recordings()), [])

    def test_remove_recording(self):
        remove_recording("test")

    def test_filelock(self):
        from home import filelock

        with filelock.FileLock("test.lock"):
            pass
