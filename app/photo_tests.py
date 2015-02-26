import unittest


class Test_Photo(unittest.TestCase):
    def _prep_photo(self):
        with open("test_data/sample1.jpg", "rb") as fp:
            return fp.read()

    def test_photo(self):
        import photo

        s = self._prep_photo()
        photo.Photo(s)

if __name__ == "__main__":
    unittest.main()