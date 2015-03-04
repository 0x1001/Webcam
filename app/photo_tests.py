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
        img_path = os.path.join(tempfile.gettempdir(), p.name)
        self.assertTrue(os.path.isfile(img_path))
        os.unlink(img_path)

        p.get_base64_contents()
        p.get_contents()

if __name__ == "__main__":
    unittest.main()