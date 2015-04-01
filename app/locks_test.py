import unittest


class TestLock(unittest.TestCase):
    def test_SocketLock(self):
        import locks

        with locks.SocketLock(64511):
            l = locks.SocketLock(64511)
            self.assertFalse(l.acquire(False))

        with locks.SocketLock(64511):
            pass

    def test_FileLock(self):
        import locks

        with locks.FileLock("test"):
            l = locks.FileLock("test")
            self.assertFalse(l.acquire(False))

        with locks.FileLock("test"):
            pass


if __name__ == "__main__":
    unittest.main()