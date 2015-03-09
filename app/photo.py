_THUMBNAIL_SIZE = 320, 180


class Photo(object):
    def __init__(self, stream):
        self.name = None
        self.time = None
        self.thumbnail = None

        self._set_attrs()
        self._photo_data = stream

    def save(self, path):
        import os

        file_path = os.path.join(path, self.name)
        thumbnail_path = os.path.join(path, self.thumbnail)
        self._save(file_path, self._photo_data)
        self._save(thumbnail_path, self._thumbnail(_THUMBNAIL_SIZE))

    def _save(self, file_path, data):
        with open(file_path, "wb") as out:
            out.write(data)

    def _thumbnail(self, size):
        import StringIO
        from PIL import Image

        im = Image.open(StringIO.StringIO(self._photo_data))
        im.thumbnail(size, Image.ANTIALIAS)
        output = StringIO.StringIO()
        im.save(output, "JPEG")

        return output.getvalue()

    def get_contents(self, size=None):

        if None:
            return self._photo_data
        else:
            return self._thumbnail(size)

    def get_base64_contents(self, size=None):
        import base64

        if None:
            return base64.b64encode(self._photo_data)
        else:
            return base64.b64encode(self._thumbnail(size))

    def _set_attrs(self):
        import datetime
        import timezone

        self.time = datetime.datetime.utcnow()
        self.time = self.time.replace(tzinfo=timezone.utc)
        self.name = self.time.strftime("%Y%m%d%H%M%S%f.jpeg")
        self.thumbnail = self.time.strftime("%Y%m%d%H%M%S%f_t.jpeg")
