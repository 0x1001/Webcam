from django.test import TestCase
from home.models import get_recordings
from home.models import remove_recording
from home.models import set_stream
from home.models import get_stream


class FunctionTests(TestCase):

    def test_get_recordings(self):
        self.assertEqual(list(get_recordings()), [])

    def test_remove_recording(self):
        remove_recording("test")

    def test_stream(self):
        import datetime

        set_stream("test", datetime.datetime.utcnow())
        get_stream()