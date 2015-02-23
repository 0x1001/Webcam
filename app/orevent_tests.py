import unittest


class Test_OrEvent(unittest.TestCase):
    def test_orevent(self):
        import threading
        import orevent
        import time

        e1 = threading.Event()
        e2 = threading.Event()

        e = orevent.OrEvent(e1, e2)

        def _e1_thread():
            e1.wait()

        def _e2_thread():
            e2.wait()

        def _e_thread():
            e.wait()

        t1 = threading.Thread(target=_e1_thread)
        t1.setDaemon(True)
        t1.start()
        t2 = threading.Thread(target=_e2_thread)
        t2.setDaemon(True)
        t2.start()
        t = threading.Thread(target=_e_thread)
        t.setDaemon(True)
        t.start()

        time.sleep(0.2)

        self.assertTrue(t1.is_alive())
        self.assertTrue(t2.is_alive())
        self.assertTrue(t.is_alive())

        time.sleep(0.2)
        e1.set()
        time.sleep(0.2)

        self.assertFalse(t1.is_alive())
        self.assertTrue(t2.is_alive())
        self.assertFalse(t.is_alive())

        time.sleep(0.2)
        e2.set()
        time.sleep(0.2)

        self.assertFalse(t1.is_alive())
        self.assertFalse(t2.is_alive())
        self.assertFalse(t.is_alive())

    def test_orevent_isset(self):
        import threading
        import orevent

        e1 = threading.Event()
        e2 = threading.Event()

        e = orevent.OrEvent(e1, e2)

        self.assertFalse(e.isset())
        self.assertFalse(e.is_set())

        e1.set()

        self.assertTrue(e.is_set())
        self.assertTrue(e.isset())

    def test_orevent_reuse(self):
        import threading
        import orevent

        e1 = threading.Event()
        e2 = threading.Event()

        e = orevent.OrEvent(e1, e2)

        with self.assertRaises(orevent.OrEventException):
            orevent.OrEvent(e1, e2)

        self.assertFalse(e.isset())
        self.assertFalse(e.is_set())

        e1.set()

        self.assertTrue(e.is_set())
        self.assertTrue(e.isset())


if __name__ == "__main__":
    unittest.main()