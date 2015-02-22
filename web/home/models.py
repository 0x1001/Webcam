from django.db import models


class Motion(models.Model):
    time = models.DateTimeField()


class Recording(models.Model):
    name = models.CharField(max_length=20)
    motion = models.ForeignKey(Motion)


def add_recording(file_name, time):
    m = Motion(time=time)
    m.save()

    r = Recording(name=file_name, motion=m)
    r.save()