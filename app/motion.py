_THRESHOLD = 1
_CMP_SIZE = (320, 240)


class Motion(object):
    def __init__(self):
        self._previous_contents = None

    def detect(self, data):
        from PIL import Image

        basic_img = self._crop(Image.open(data))
        gray_img = self._gray_scale(basic_img)
        float_img = self._get_float_data(gray_img)
        norm_img = self._normalize(float_img)

        if self._previous_contents is None:
            value = 0.0
            self._previous_contents = norm_img
        else:
            value = self._diff(self._previous_contents, norm_img)
            self._previous_contents = norm_img

        return value > _THRESHOLD

    def _crop(self, image):
        image.thumbnail(_CMP_SIZE)
        return image

    def _gray_scale(self, image):
        return image.convert("L")

    def _get_float_data(self, image):
        return image.convert("F").getdata()

    def _normalize(self, data):
        return [d / 255 for d in data]

    def _diff(self, data1, data2):
        if len(data1) != len(data2):
            raise Exception("Size don't match!")

        matt_norm = sum([abs(data1[i] - data2[i]) for i in range(len(data1))])
        return matt_norm / len(data1) * 100