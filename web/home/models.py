from django.db import models
import datetime


class Photo(models.Model):
    name = models.CharField(max_length=20, unique=True)
    time = models.DateTimeField(default=datetime.datetime(year=1999, month=1, day=1))
    thumbnail = models.CharField(max_length=20, unique=True, default="nophoto")


class Recording(models.Model):
    name = models.CharField(max_length=20, unique=True)
    time = models.DateTimeField(default=datetime.datetime(year=1999, month=1, day=1))
    lenght = models.IntegerField(default=0)
    photo = models.ForeignKey(Photo)


class Movement(models.Model):
    time = models.DateTimeField(unique=True)
    photo = models.ForeignKey(Photo)
    recording = models.ForeignKey(Recording)


def add_photo(name, thumbnail, time):
    Photo(name=name, thumbnail=thumbnail, time=time).save()


def add_recording(name, time, lenght, photo):
    p = Photo.objects.filter(name=photo).first()
    Recording(name=name, time=time, lenght=lenght, photo=p).save()


def add_movement(time, recording, photo):
    p = Photo.objects.filter(name=photo).first()
    r = Recording.objects.filter(name=recording).first()
    Movement(time=time, recording=r, photo=p).save()


def get_recordings():
    return Recording.objects.exclude(name="norecording").order_by('-time').all()


def get_photos():
    return Photo.objects.exclude(name="nophoto").order_by('-time').all()


def remove_recording(name):
    r = _get_no_recording()
    Movement.objects.filter(recording__name=name).update(recording=r)
    Recording.objects.filter(name=name).delete()


def remove_photo(name):
    p = _get_no_photo()

    Movement.objects.filter(photo__name=name).update(photo=p)
    Photo.objects.filter(name=name).delete()


def _get_no_recording():
    p = _get_no_photo()
    r = Recording.objects.filter(name="norecording").first()
    if r is None:
        r = Recording(name="norecording", photo=p)
        r.save()

    return r


def _get_no_photo():
    p = Photo.objects.filter(name="nophoto").first()
    if p is None:
        p = Photo(name="nophoto")
        p.save()

    return p