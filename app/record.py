def record():
    import picamera
    import io

    stream = io.BytesIO()

    print "1"
    camera = picamera.PiCamera()
    print "2"
    camera.resolution = (640, 480)
    print "3"
    camera.start_recording(stream, format='mjpeg')
    print "4"
    camera.wait_recording(10)
    print "5"
    camera.stop_recording()
    print "6"

    with open('my_video.mp4', "wb") as output:
        output.write(stream.getvalue())

    print "7"