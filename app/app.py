# This whole multiprocessing thing is because of small memory leak.
# Every few hours or days webcam has to be restarted.
# This is very unfortunate.

import multiprocessing

stop = multiprocessing.Event()


def _ignor_signal():
    """
        Multiprocessing dosent work well with signals.
        This function is used to ignore keyboard interrupt in child process.
    """
    import signal
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def webcam():
    import threading
    import rpiwebcam

    _ignor_signal()

    webcam = rpiwebcam.RPiWebcam()

    record_motion = threading.Thread(target=webcam.record_motion)
    record_motion.start()

    cleaner = threading.Thread(target=webcam.clean)
    cleaner.start()

    stream = threading.Thread(target=webcam.stream)
    stream.setDaemon(True)
    stream.start()

    stop.wait()

    webcam.close()
    record_motion.join()
    cleaner.join()


def _configure_exit(exit_event):
    import signal

    def _signal_handler(signal, frame):
        print 'Exiting...'
        exit_event.set()

    signal.signal(signal.SIGINT, _signal_handler)
    print 'Press Ctrl+C to exit'
    signal.pause()


def app_thread(exit_event):
    while not exit_event.is_set():
        p = multiprocessing.Process(target=webcam)
        p.start()
        exit_event.wait(24 * 3600)
        stop.set()
        p.join()
        stop.clear()

if __name__ == "__main__":
    import threading

    exit_event = threading.Event()

    app = threading.Thread(target=app_thread, args=(exit_event,))
    app.start()

    _configure_exit(exit_event)

    app.join()
