import unittest


class Test_motion(unittest.TestCase):
    def test_motion_detect(self):
        import motion
        from StringIO import StringIO

        m = motion.Motion()

        image1 = StringIO(open("test_data/sample1.jpg", "rb").read())
        image2 = StringIO(open("test_data/sample2.jpg", "rb").read())
        image3 = StringIO(open("test_data/sample2.jpg", "rb").read())

        self.assertFalse(m.detect(image1))
        self.assertTrue(m.detect(image2), 0)
        self.assertFalse(m.detect(image3), 0)

if __name__ == "__main__":
    unittest.main()