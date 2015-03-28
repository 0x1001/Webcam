from django.shortcuts import render
from django.shortcuts import redirect
from home.models import get_movements
from home.models import get_recordings
from home.models import get_photos
from django.core.servers.basehttp import FileWrapper
from django.http import StreamingHttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def recordings(request, recording=None, page=1):
    page = int(page)

    recordings_all = get_recordings()
    paginator = Paginator(recordings_all, 20)

    try:
        recordings = paginator.page(page)
    except PageNotAnInteger:
        recordings = paginator.page(1)
    except EmptyPage:
        recordings = paginator.page(paginator.num_pages)

    if recording is None and len(recordings.object_list) != 0:
        recording = recordings[0].name

    return render(request, 'recordings.html', {"recordings": recordings, "recording": recording})


def photos(request, photo=None, page=1):
    page = int(page)

    photos_all = get_photos()
    paginator = Paginator(photos_all, 20)

    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)

    if photo is None and len(photos.object_list) != 0:
        photo = photos.object_list[0].name

    return render(request, 'photos.html', {"photos": photos, "photo": photo})


def movements(request, page=1):
    page = int(page)

    mov_all = get_movements()
    paginator = Paginator(mov_all, 50)

    try:
        movements = paginator.page(page)
    except PageNotAnInteger:
        movements = paginator.page(1)
    except EmptyPage:
        movements = paginator.page(paginator.num_pages)

    return render(request, 'movements.html', {"movements": movements})


def stream(request):
    return render(request, 'stream.html')


def stream_data(request):
    from gevent import socket

    s = socket.create_connection(("127.0.0.1", 1234))
    sf = s.makefile()

    return StreamingHttpResponse(FileWrapper(sf), content_type='text/plain')


def configuration(request):
    return render(request, 'configuration.html')


def restart_app(request):
    import subprocess
    import os
    import time

    current_path = os.path.abspath(__file__)
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))

    stop_cmd = [os.path.join(base_path, "webcam.sh"), "stop", "app"]
    start_cmd = [os.path.join(base_path, "webcam.sh"), "start", "app"]

    subprocess.Popen(stop_cmd, cwd=base_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True).wait()
    time.sleep(2)
    subprocess.Popen(start_cmd, cwd=base_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

    return redirect('home.views.configuration')


def restart_pi(request):
    import subprocess

    cmd = ["reboot"]
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

    return redirect('home.views.configuration')


def shutdown_pi(request):
    import subprocess

    cmd = ["shutdown", "-h", "now"]
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

    return redirect('home.views.configuration')