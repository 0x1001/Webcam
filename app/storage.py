class StorageExcpetion(Exception):
    pass


class Storage(object):
    def save_recording(self, recording):
        import datetime
        import timezone

        now = datetime.datetime.utcnow()
        now = now.replace(tzinfo=timezone.utc)
        name = now.strftime("%Y%m%d%H%M%S")
        output_path = self._output_path(name)

        self._save(recording, output_path)
        file_name = self._convert(output_path)
        self._add_to_database(file_name, now)

    def _save(self, data, output_path):
        h264_path = output_path + ".h264"
        with open(h264_path, "wb") as output:
            output.write(data)

    def _convert(self, output_path):
        import subprocess
        import os

        mp4_path = output_path + ".mp4"
        h264_path = output_path + ".h264"
        cmd = "MP4Box -fps 30 -add " + h264_path + " " + mp4_path

        ret = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if ret != 0:
            raise StorageExcpetion("Convertion to mp4 failed on " + output_path)

        os.unlink(h264_path)
        return os.path.basename(mp4_path)

    def _add_to_database(self, file_name, time):
        from home.models import add_recording

        add_recording(file_name, time)

    def _output_path(self, name):
        import os
        from webcam import settings

        return os.path.join(settings.STATICFILES_DIRS[0], name)