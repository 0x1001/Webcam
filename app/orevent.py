class OrEventException(Exception):
    pass


class OrEvent(object):
    def __init__(self, *events):
        import threading

        self._events = events
        for e in self._events:
            if hasattr(e, "_orevent"):
                raise OrEventException("There can be only one OrEvent registerd for given events!")
            else:
                e._orevent = None

        self._event = threading.Event()

        def changed():
            bools = [e.is_set() for e in self._events]
            if any(bools):
                self._event.set()
            else:
                self._event.clear()

        for e in self._events:
            self._orify(e, changed)

        changed()

    def is_set(self):
        return self._event.is_set()

    isset = is_set

    def wait(self, *args, **kwargs):
        return self._event.wait(*args, **kwargs)

    def _or_set(self, e):
        e._set()
        e.changed()

    def _or_clear(self, e):
        e._clear()
        e.changed()

    def _orify(self, e, changed_callback):
        e._set = e.set
        e._clear = e.clear
        e.changed = changed_callback
        e.set = lambda: self._or_set(e)
        e.clear = lambda: self._or_clear(e)

    def close(self):
        for e in self._events:
            e.set = e._set
            e.clear = e._clear
            del e._set
            del e._clear
            del e.changed
            del e._orevent

        self._events = []
