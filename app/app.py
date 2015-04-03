def _configure_exit(webcam):
    import signal

    def _signal_handler(signal, frame):
        print 'Exiting...'
        webcam.close()

    signal.signal(signal.SIGINT, _signal_handler)
    print 'Press Ctrl+C to exit'
    signal.pause()


def _debug():
    from pympler import summary
    import sys
    import time
    import datetime
    import StringIO
    import gc

    while True:
        temp = sys.stdout
        sys.stdout = StringIO.StringIO()
        summary.print_(summary.summarize(gc.get_objects()))
        report = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = temp

        with open("report_" + str(datetime.datetime.now()) + ".txt", "w") as fp:
            fp.write(report)

        time.sleep(600)

if __name__ == "__main__":
    import threading
    import rpiwebcam

    webcam = rpiwebcam.RPiWebcam()

    record_motion = threading.Thread(target=webcam.record_motion)
    record_motion.start()

    cleaner = threading.Thread(target=webcam.clean)
    cleaner.start()

    stream = threading.Thread(target=webcam.stream)
    stream.setDaemon(True)
    stream.start()

    #_debug_thread = threading.Thread(target=_debug)
    #_debug_thread.setDaemon(True)
    #_debug_thread.start()

    _configure_exit(webcam)

    record_motion.join()
    cleaner.join()
