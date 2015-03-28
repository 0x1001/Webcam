class FileLock(object):
    def __init__(self, filename):
        import os

        self.filename = filename
        self.fd = None
        self.pid = os.getpid()

    def acquire(self, blocking=True):
        import time
        import random

        while True:
            if self._acquire():
                return True
            elif blocking:
                time.sleep(random.random() * 2)
            else:
                return False

    def _acquire(self):
        import os
        try:
            self.fd = os.open(self.filename, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.write(self.fd, "%d" % self.pid)
            return True
        except OSError:
            return False

    def release(self):
        import os

        if self.fd is None:
            return False

        try:
            os.close(self.fd)
            os.remove(self.filename)
            self.fd = None
            return True
        except OSError:
            return False

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, type, value, traceback):
        self.release()

    def __del__(self):
        self.release()
