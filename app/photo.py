_THUMBNAIL_SIZE = 128, 128


class Photo(object):
    def __init__(self, stream):
        self.name = None
        self.time = None

        self._set_attrs()
        self._photo_data = stream

    def save(self, path):
        import os

        file_path = os.path.join(path, self.name)
        with open(file_path, "wb") as out:
            out.write(self._photo_data)

    def get_contents(self):
        return self._photo_data

    def get_base64_contents(self):
        import base64

        return base64.b64encode(self._photo_data)

    def _set_attrs(self):
        import datetime
        import timezone

        self.time = datetime.datetime.utcnow()
        self.time = self.time.replace(tzinfo=timezone.utc)
        self.name = self.time.strftime("%Y%m%d%H%M%S%f.jpeg")
