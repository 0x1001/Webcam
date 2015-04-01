class SocketLock(object):

    def __init__(self, name):
        self._name = self._generate_name(name)
        self._socket = None

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

    def release(self):
        if self._socket is None:
            return False

        self._socket.close()

    def _acquire(self):
        import socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self._socket.bind(('127.0.0.1', self._name))
        except socket.error:
            self._socket.close()
            self._socket = None
            return False

        return True

    def _generate_name(self, name):
        return hash(name) % 64510 + 1024

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, type, value, traceback):
        self.release()

    def __del__(self):
        self.release()


class FileLock(object):
    def __init__(self, name):
        import os

        self.filename = name
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
