import unittest


class Test_Command(unittest.TestCase):
    def test_execute(self):
        import command

        c = command.Command(len, ("test",))
        self.assertEqual(c.execute(), 4)

if __name__ == "__main__":
    unittest.main()