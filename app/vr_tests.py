import unittest
from PIL import Image
import vr


class TestVR(unittest.TestCase):
    def test_motion_detect(self):
        image1 = Image.open("1.jpg")
        image2 = Image.open("2.jpg")

        image1 = vr.gray_scale(image1)
        image2 = vr.gray_scale(image2)

        data1 = vr.get_float_data(image1)
        data2 = vr.get_float_data(image2)

        data1 = vr.normalize(data1)
        data2 = vr.normalize(data2)

        vr.difference(data1, data2)

    def test_gray_scale(self):
        image1 = Image.open("1.jpg")
        vr.gray_scale(image1)

    def test_get_data(self):
        image1 = Image.open("1.jpg")
        vr.get_float_data(image1)

    def test_normalize(self):
        vr.normalize([1.0, 2.0, 3.0, 4.0])

    def test_difference(self):
        diff = vr.difference([1.0, 0.0, 0.3, 0.2], [1.0, 0.0, 0.3, 0.2])
        self.assertEqual(diff, 0)

        diff = vr.difference([1.0, 1.0, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0])
        self.assertEqual(diff, 100)

if __name__ == "__main__":
    unittest.main()