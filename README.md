# Raspberry Pi Web Camera

Raspberry Pi Web Camera is web camera build on Raspberry Pi 2 which uses Raspberry Pi Camera.

  - Interface via web page
  - Motion detection
  - Photos and Recordings

## Screenshots
- [Home page]
- [Photos]
- [Movements list]

## Version
1.1.0

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

## Todo

 - Recordings on demand
 - Photos on demand
 - Time lapse videos
 - Recording and photo schedule

## License

GNU GENERAL PUBLIC LICENSE

[Home page]:https://raw.githubusercontent.com/0x1001/Webcam/master/screenshots/home.png
[Photos]:https://raw.githubusercontent.com/0x1001/Webcam/master/screenshots/photos.png
[Movements list]:https://raw.githubusercontent.com/0x1001/Webcam/master/screenshots/movements.png

[Picamera]:http://picamera.readthedocs.org/
[NumPy]:http://www.numpy.org/
[Django]:https://www.djangoproject.com/
[Gevent]:http://gevent.org/
[Simplex]:https://bootswatch.com/simplex/
[PIL]:http://www.pythonware.com/products/pil/

