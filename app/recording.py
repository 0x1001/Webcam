class RecordingException(Exception):
    pass


class Recording(object):
    def __init__(self, stream, lenght):
        self.name = None
        self.time = None
        self.path = None
        self.lenght = lenght

        self._set_attrs()

        if isinstance(stream, str):
            self._process(stream)
        else:
            raise RecordingException("Wrong stream type: " + str(type(stream)))

    def cut(self, start, stop):
        import subprocess

        if start > stop:
            raise RecordingException("Invalid start and stop args: " + str(start) + " " + str(stop))

        cmd = "MP4Box -splitx " + str(start) + ":" + str(stop) + " " + self.path + " -out " + self.path

        ret = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if ret != 0:
            raise RecordingException("Cannot cut recording: " + self.path)

        self.lenght = stop - start

    def remove(self):
        import os

        if os.path.isfile(self.path):
            os.unlink(self.path)

    def save(self, path):
        import shutil
        import os

        shutil.copy(self.path, path)
        self.remove()

        if os.path.isfile(path):
            self.path = path
        else:
            self.path = os.path.join(path, self.name)

    def _set_attrs(self):
        import tempfile
        import datetime
        import timezone
        import os

        self.time = datetime.datetime.utcnow()
        self.time = self.time.replace(tzinfo=timezone.utc)

        self.name = self.time.strftime("%Y%m%d%H%M%S%f.mp4")
        name_h264 = self.time.strftime("%Y%m%d%H%M%S%f.h264")

        self.path = os.path.join(tempfile.gettempdir(), self.name)
        self.temp_path = os.path.join(tempfile.gettempdir(), name_h264)

    def _process(self, stream):
        import os

        with open(self.temp_path, 'wb') as out:
            out.write(stream)

        self._convert(self.temp_path, self.path)
        os.unlink(self.temp_path)

    def _convert(self, src, dst):
        import subprocess

        cmd = "MP4Box -fps 30 -add " + src + " " + dst

        ret = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if ret != 0:
            raise RecordingException("Convertion to mp4 failed on " + src)