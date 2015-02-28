from django.shortcuts import render
from home.models import Configuration
from home.models import get_recordings
from home.models import get_movements


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
