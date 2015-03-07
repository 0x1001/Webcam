class RecordingException(Exception):
    pass


class Recording(object):
    def __init__(self, stream, lenght):
        import command

        self.name = None
        self.time = None
        self.lenght = lenght
        self.path = None
        self._temp_path = None
        self._processing_list = []

        if isinstance(stream, str):
            self._stream = stream
        else:
            raise RecordingException("Wrong stream type: " + str(type(stream)))

        self._set_attrs()
        self._processing_list.append(command.Command(self._process))

    def cut(self, start, stop):
        import command

        if start > stop:
            raise RecordingException("Invalid start and stop args: " + str(start) + " " + str(stop))

        self._processing_list.append(command.Command(self._cut, (start, stop)))

    def remove(self):
        import os

        if os.path.isfile(self.path):
            os.unlink(self.path)

    def save(self, path):
        import os

        if not os.path.isdir(path):
            raise RecordingException("Input path does not exist or is not a folder: " + path)

        self.path = os.path.join(path, self.name)

        for command in self._processing_list:
            command.execute()

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
        self._temp_path = os.path.join(tempfile.gettempdir(), name_h264)

    def _process(self):
        import os

        with open(self._temp_path, 'wb') as out:
            out.write(self._stream)

        self._convert(self._temp_path, self.path)
        os.unlink(self._temp_path)

    def _convert(self, src, dst):
        import subprocess

        cmd = "MP4Box -fps 30 -add " + src + " " + dst

        ret = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if ret != 0:
            raise RecordingException("Convertion to mp4 failed on " + src)

    def _cut(self, start, stop):
        import subprocess

        cmd = "MP4Box -splitx " + str(start) + ":" + str(stop) + " " + self.path + " -out " + self.path

        ret = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if ret != 0:
            raise RecordingException("Cannot cut recording: " + self.path)

        self.lenght = stop - start