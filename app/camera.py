import io
import picamera
from PIL import Image
import vr

prior_image = None


def detect_motion(camera):
    print "Detecting..."
    global prior_image
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg', use_video_port=True)
    stream.seek(0)
    if prior_image is None:
        prior_image = Image.open(stream)
        prior_image.thumbnail((320, 240))
        return False
    else:
        print "Calculating diff..."
        current_image = Image.open(stream)
        current_image.thumbnail((320, 240))
        # Compare current_image to prior_image to detect motion. This is
        # left as an exercise for the reader!
        one = vr.normalize(vr.get_float_data(vr.gray_scale(current_image)))
        two = vr.normalize(vr.get_float_data(vr.gray_scale(prior_image)))
        diff = vr.difference(one, two)
        print "Difference: " + str(diff)

        if diff > 1:
            result = True
        else:
            result = False
        # Once motion detection is done, make the prior image the current
        prior_image = current_image
        return result


def write_video(stream):
    # Write the entire content of the circular buffer to disk. No need to
    # lock the stream here as we're definitely not writing to it
    # simultaneously
    with io.open('before.h264', 'wb') as output:
        for frame in stream.frames:
            if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break
        while True:
            buf = stream.read1()
            if not buf:
                break
            output.write(buf)
    # Wipe the circular stream once we're done
    stream.seek(0)
    stream.truncate()

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.led = False
    stream = picamera.PiCameraCircularIO(camera, seconds=10)
    camera.start_recording(stream, format='h264')
    try:
        while True:
            camera.wait_recording(0.2)
            if detect_motion(camera):
                camera.led = True
                print('Motion detected!')
                # As soon as we detect motion, split the recording to
                # record the frames "after" motion
                camera.split_recording('after.h264')
                # Write the 10 seconds "before" motion to disk as well
                write_video(stream)
                # Wait until motion is no longer detected, then split
                # recording back to the in-memory circular buffer
                while detect_motion(camera):
                    camera.wait_recording(0.2)
                print('Motion stopped!')
                camera.led = False
                camera.split_recording(stream)
    finally:
        camera.stop_recording()