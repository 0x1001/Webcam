class StorageExcpetion(Exception):
    pass


class Storage(object):
    def save_recording(self, recording):
        import datetime
        import timezone
        import os

        now = datetime.datetime.utcnow()
        now = now.replace(tzinfo=timezone.utc)
        name = now.strftime("%Y%m%d%H%M%S")

        mp4_path, h264_path = self._output_path(name)

        self._save(recording, h264_path)
        self._convert(h264_path, mp4_path)
        self._add_to_database(os.path.basename(mp4_path), now)

        os.unlink(h264_path)

    def _save(self, data, output_path):
        with open(output_path, "wb") as output:
            output.write(data)

    def _convert(self, src, dst):
        import subprocess

        cmd = "MP4Box -fps 30 -add " + src + " " + dst

        ret = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if ret != 0:
            raise StorageExcpetion("Convertion to mp4 failed on " + src)

    def _add_to_database(self, file_name, time):
        from home.models import add_recording

        add_recording(file_name, time)

    def _output_path(self, name):
        import os
        from webcam import settings

        mp4_path = os.path.join(settings.STATICFILES_DIRS[0], name + ".mp4")
        h264_path = os.path.join(settings.STATICFILES_DIRS[0], name + ".h264")

        return mp4_path, h264_path