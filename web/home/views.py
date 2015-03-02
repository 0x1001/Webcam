from django.shortcuts import render
from home.models import Configuration
from home.models import Movement
from home.models import get_recordings
from django.core.servers.basehttp import FileWrapper
from django.http import StreamingHttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'home.html')


def recordings(request, recording=None):
    return render(request, 'recordings.html', {"recordings": get_recordings(), "recording": recording})


def movements(request, page=1):
    page = int(page)

    mov_all = Movement.objects.order_by('-time').all()
    paginator = Paginator(mov_all, 100)

    try:
        movements = paginator.page(page)
    except PageNotAnInteger:
        movements = paginator.page(1)
    except EmptyPage:
        movements = paginator.page(paginator.num_pages)

    return render(request, 'movements.html', {"movements": movements})


def get_config(request):
    return render(request, 'configuration.html', {"config": Configuration.objects.first()})


def stream(request):
    return render(request, 'stream.html')


def stream_data(request):
    from gevent import socket
    from time import sleep

    sleep(0.5)
    s = socket.create_connection(("127.0.0.1", 1234))
    sf = s.makefile()

    return StreamingHttpResponse(FileWrapper(sf), content_type='text/plain')