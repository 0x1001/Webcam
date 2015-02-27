from django.db import models


class Photo(models.Model):
    name = models.CharField(max_length=20)
    thumbnail = models.CharField(max_length=20)
    time = models.DateTimeField()


class Recording(models.Model):
    name = models.CharField(max_length=20)
    time = models.DateTimeField()
    lenght = models.IntegerField()
    photo = models.OneToOneField(Photo)


class Movement(models.Model):
    time = models.DateTimeField()
    photo = models.OneToOneField(Photo)
    recording = models.OneToOneField(Recording)


class Configuration(models.Model):
    width = models.IntegerField(default=800)
    height = models.IntegerField(default=600)
    hflip = models.BooleanField(default=False)


def add_photo(name, thumbnail_name, time):
    Photo(name=name, thumbnail=thumbnail_name, time=time).save()


def add_recording(name, time, lenght, photo):
    p = Photo.objects.filter(name=photo).first()
    Recording(name=name, time=time, lenght=lenght, photo=p).save()


def add_movement(time, recording, photo):
    p = Photo.objects.filter(name=photo).first()
    r = Recording.objects.filter(name=recording).first()
    Movement(time=time, recording=r, photo=p).save()


def get_recordings():
    return Recording.objects.order_by('-time').all()


def remove_recording(name):
    #Recording.objects.filter(name=name).delete()
    raise NotImplemented
