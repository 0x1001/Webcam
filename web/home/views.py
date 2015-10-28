from django.shortcuts import render
from django.shortcuts import redirect
from home.models import get_movements
from home.models import get_movement
from django.core.servers.basehttp import FileWrapper
from django.http import StreamingHttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def movements(request, page=1):
    page = int(page)

    mov_all = get_movements()
    paginator = Paginator(mov_all, 52)

    try:
        movements = paginator.page(page)
    except PageNotAnInteger:
        movements = paginator.page(1)
    except EmptyPage:
        movements = paginator.page(paginator.num_pages)

    return render(request, 'movements.html', {"movements": movements})


def movement_details(request, movement_id):
    movement = get_movement(movement_id)
    return render(request, 'movement_details.html', {"movement": movement})


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