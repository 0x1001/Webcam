from django.db import models


class Motion(models.Model):
    time = models.DateTimeField()


class Recording(models.Model):
    name = models.CharField(max_length=20)
    time = models.DateTimeField()


class Configuration(models.Model):
    width = models.IntegerField(default=800)
    height = models.IntegerField(default=600)
    hflip = models.BooleanField(default=False)


def add_recording(file_name, time):
    r = Recording(name=file_name, time=time)
    r.save()


def get_recordings():
    return Recording.objects.order_by('-time').all()


def remove_recording(name):
    Recording.objects.filter(name=name).delete()