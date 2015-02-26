class StorageExcpetion(Exception):
    pass


class Storage(object):
    def __init__(self):
        self._init_django()

    def save_recording(self, recording):
        self._save(recording)
        self._add_recording_to_database(recording)
        recording.remove()

    def get_all_recordings(self):
        from home.models import get_recordings

        return list(get_recordings())

    def delete_recording(self, name):
        self._delete(name)
        self._remove_recording_from_database(name)

    def save_stream(self, photo):
        with open(self._photo_output_path("stream"), "wb") as out:
            out.write(photo)

    def _delete(self, name):
        from webcam import settings
        import os

        path = os.path.join(settings.STATICFILES_DIRS[0], name)
        if os.path.isfile(path):
            os.unlink(path)

    def _remove_recording_from_database(self, name):
        from home.models import remove_recording

        remove_recording(name)

    def _save(self, recording):
        import shutil
        from webcam import settings

        shutil.copy(recording.path, settings.STATICFILES_DIRS[0])

    def _add_recording_to_database(self, recording):
        from home.models import add_recording

        add_recording(recording.name, recording.time)

    def _photo_output_path(self, name):
        import os
        from webcam import settings

        return os.path.join(settings.STATICFILES_DIRS[1], name + ".jpeg")

    def _init_django(self):
        from os import environ
        from os.path import join, dirname, abspath
        import sys
        import django

        environ['DJANGO_SETTINGS_MODULE'] = 'webcam.settings'
        sys.path.append(join(dirname(dirname(abspath(__file__))), "web"))
        django.setup()