_THUMBNAIL_SIZE = 128, 128


class Photo(object):
    def __init__(self, stream):
        self.name = None
        self.thumbnail_name = None
        self.time = None

        self._set_attrs()
        self._stream = stream
        self._thumbnail = self._create_thumbnail(stream)

    def save(self, path):
        import os

        file_path = os.path.join(path, self.name)
        self._save(file_path)

    def save_thumbnail(self, path):
        import os

        file_path = os.path.join(path, self.thumbnail_name)
        if not os.path.isfile(file_path):
            self._save(file_path)

    def _save(self, file_path):
        with open(file_path, "wb") as out:
            out.write(self.stream)

    def _create_thumbnail(self, stream):
        from PIL import Image
        import io
        import StringIO

        img = Image.open(io.BytesIO(stream))
        img.thumbnail(_THUMBNAIL_SIZE)
        out = StringIO.StringIO()
        img.save(out, img.format)
        out.seek(0)
        return out.read()

    def _set_attrs(self):
        import datetime
        import timezone

        self.time = datetime.datetime.utcnow()
        self.time = self.time.replace(tzinfo=timezone.utc)

        self.name = self.time.strftime("%Y%m%d%H%M%S%f.jpeg")
        self.thumbnail_name = self.time.strftime("%Y%m%d%H%M%S%f_t.jpeg")
