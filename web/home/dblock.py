import imp
import os

locks_path = os.path.join(
                          os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                          "app",
                          "locks.py")

locks = imp.load_source("locks", locks_path)


class DBLock(locks.SocketLock):
    def __init__(self):
        super(DBLock, self).__init__(64510)
