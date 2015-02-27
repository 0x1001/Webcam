_THUMBNAIL_SIZE = 128, 128


class Photo(object):
    def __init__(self, stream):
        self.name = None
        self.thumbnail_name = None
        self.time = None

        self._set_attrs()
        self._photo_data = stream
        self._thumbnail_data = self._create_thumbnail(self._photo_data)

    def save(self, path):
        import os

        file_path = os.path.join(path, self.name)
        self._save(self._photo_data, file_path)

    def save_thumbnail(self, path):
        import os

        file_path = os.path.join(path, self.thumbnail_name)
        self._save(self._thumbnail_data, file_path)

    def _save(self, stream, file_path):
        with open(file_path, "wb") as out:
            out.write(stream)

    def _create_thumbnail(self, stream):
        from PIL import Image
        import StringIO

        img = Image.open(StringIO.StringIO(stream))
        img.thumbnail(_THUMBNAIL_SIZE, Image.ANTIALIAS)
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
