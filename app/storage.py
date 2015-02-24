class StorageExcpetion(Exception):
    pass


class Storage(object):
    def __init__(self):
        self._init_django()

    def save_recording(self, recording):
        import datetime
        import timezone
        import os

        now = datetime.datetime.utcnow()
        now = now.replace(tzinfo=timezone.utc)
        name = now.strftime("%Y%m%d%H%M%S")

        mp4_path, h264_path = self._recording_output_path(name)

        self._save(recording, h264_path)
        self._convert(h264_path, mp4_path)
        self._add_recording_to_database(os.path.basename(mp4_path), now)

        os.unlink(h264_path)

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
        import os

        path, _ = self._recording_output_path(os.path.splitext(name)[0])
        if os.path.isfile(path):
            os.path.unlink(path)

    def _remove_recording_from_database(self, name):
        from home.models import remove_recording

        remove_recording(name)

    def _save(self, data, output_path):
        with open(output_path, "wb") as output:
            output.write(data)

    def _convert(self, src, dst):
        import subprocess

        cmd = "MP4Box -fps 30 -add " + src + " " + dst

        ret = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if ret != 0:
            raise StorageExcpetion("Convertion to mp4 failed on " + src)

    def _add_recording_to_database(self, file_name, time):
        from home.models import add_recording

        add_recording(file_name, time)

    def _recording_output_path(self, name):
        import os
        from webcam import settings

        mp4_path = os.path.join(settings.STATICFILES_DIRS[0], name + ".mp4")
        h264_path = os.path.join(settings.STATICFILES_DIRS[0], name + ".h264")

        return mp4_path, h264_path

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