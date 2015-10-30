# Raspberry Pi Web Camera

Raspberry Pi Web Camera is web camera build on Raspberry Pi 2 which uses Raspberry Pi Camera.

  - Interface via web page
  - Motion detection
  - Photos and Recordings

## Screenshots and Photos
- [Home page]
- [Movements list]
- [Webcam device]

## Version
1.2.0

## List of third party libraries
- [Picamera]
- [NumPy]
- [Django]
- [Gevent]
- [Simplex]
- [PIL]

## Installation

You need to get this repo to your Raspberry Pi by doing:
```sh
$ git clone https://github.com/0x1001/Webcam.git
```
Then run installer:
```sh
$ cd Webcam
$ ./install.sh
```
Activate Raspberry Pi Camera if you haven't done that yet:
```sh
$ sudo raspi-config
```

## Starting and Stopping

```sh
$ sudo ./webcam.sh start
```

```sh
$ sudo ./webcam.sh stop
```

## Change log
- 1.3.0
    - Adding exception handling for camera and recordings
    - Recordings and photos pages merged together as movements page
    - Fixing bug in storage. Occasional OSError
    - Adding auto refresh for Live stream page
    
- 1.2.0
    - Change to motion detection algorithm
    - Adding images of camera device
    - Bug fix: Workaround for memory leak in picamera

- 1.1.0
    - Adding lock to protect database access
    - Bug fix: Photo stream sometimes was None
    - Bug fix: Recording memory leak fix

- 1.0.0
    - Initial version
    - Motion detection with video recordings
    - Web page interface
    - Raspberry PI Camera support

## Want to contribute?

Anyone is welcome to contribute to this project :).
Just contact me on Github.

## License

GNU GENERAL PUBLIC LICENSE

[Home page]:https://raw.githubusercontent.com/0x1001/Webcam/master/screenshots/home.png
[Movements list]:https://raw.githubusercontent.com/0x1001/Webcam/master/screenshots/movements.png
[Webcam device]:https://raw.githubusercontent.com/0x1001/Webcam/master/screenshots/IMG_20150426_144456.jpg

[Picamera]:http://picamera.readthedocs.org/
[NumPy]:http://www.numpy.org/
[Django]:https://www.djangoproject.com/
[Gevent]:http://gevent.org/
[Simplex]:https://bootswatch.com/simplex/
[PIL]:http://www.pythonware.com/products/pil/

