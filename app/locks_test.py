import unittest


class TestLock(unittest.TestCase):
    def test_lock(self):
        import locks

        with locks.SocketLock(64511):
            l = locks.SocketLock(64511)
            self.assertFalse(l.acquire(False))

        with locks.SocketLock(64511):
            pass


if __name__ == "__main__":
    unittest.main()