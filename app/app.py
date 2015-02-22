def _configure_exit(webcam):
    import signal

    def _signal_handler(signal, frame):
        print 'Exiting...'
        webcam.close()

    signal.signal(signal.SIGINT, _signal_handler)
    print 'Press Ctrl+C to exit'
    signal.pause()


def _configure_django():
    from os import environ
    from os.path import join, dirname, abspath
    import sys
    import django

    environ['DJANGO_SETTINGS_MODULE'] = 'webcam.settings'
    sys.path.append(join(dirname(dirname(abspath(__file__))), "web"))
    django.setup()

if __name__ == "__main__":
    import threading
    import rpiwebcam

    _configure_django()

    webcam = rpiwebcam.RPiWebcam()
    record_motion = threading.Thread(target=webcam.record_motion)
    record_motion.start()

    _configure_exit(webcam)
    record_motion.join()
