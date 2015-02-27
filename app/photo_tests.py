import unittest


class Test_Photo(unittest.TestCase):
    def _prep_photo(self):
        with open("test_data/sample1.jpg", "rb") as fp:
            return fp.read()

    def test_photo(self):
        import photo
        import tempfile
        import os

        s = self._prep_photo()
        p = photo.Photo(s)
        p.save(tempfile.gettempdir())
        p.save_thumbnail(tempfile.gettempdir())

        img_path = os.path.join(tempfile.gettempdir(), p.name)
        t_image_path = os.path.join(tempfile.gettempdir(), p.thumbnail_name)

        self.assertTrue(os.path.isfile(img_path))
        self.assertTrue(os.path.isfile(t_image_path))

        img_size = os.path.getsize(img_path)
        t_img_size = os.path.getsize(t_image_path)

        self.assertGreater(img_size, t_img_size)

        os.unlink(img_path)
        os.unlink(t_image_path)

if __name__ == "__main__":
    unittest.main()