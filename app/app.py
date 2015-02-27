def _configure_exit(webcam):
    import signal

    def _signal_handler(signal, frame):
        print 'Exiting...'
        webcam.close()

    signal.signal(signal.SIGINT, _signal_handler)
    print 'Press Ctrl+C to exit'
    signal.pause()


if __name__ == "__main__":
    import threading
    import rpiwebcam

    webcam = rpiwebcam.RPiWebcam()

    record_motion = threading.Thread(target=webcam.record_motion)
    record_motion.start()

    cleaner = threading.Thread(target=webcam.clean)
    cleaner.start()

    #stream = threading.Thread(target=webcam.stream)
    #stream.start()

    _configure_exit(webcam)

    record_motion.join()
    cleaner.join()
    #stream.join()
