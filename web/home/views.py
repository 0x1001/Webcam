from django.shortcuts import render
from home.models import Configuration
from home.models import get_recordings
from home.models import get_movements
from django.core.servers.basehttp import FileWrapper
from django.http import StreamingHttpResponse


def home(request):
    return render(request, 'home.html')


def recordings(request, recording=None):
    return render(request, 'recordings.html', {"recordings": get_recordings(), "recording": recording})


def movements(request):
    return render(request, 'movements.html', {"movements": get_movements()})


def get_config(request):
    return render(request, 'configuration.html', {"config": Configuration.objects.first()})


def stream(request):
    return render(request, 'stream.html')


def stream_data(request):
    from gevent import socket
    from time import sleep

    sleep(0.3)
    s = socket.create_connection(("127.0.0.1", 1234))
    sf = s.makefile()

    return StreamingHttpResponse(FileWrapper(sf), content_type='image/jpeg')