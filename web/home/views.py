from django.shortcuts import render
from home.models import Configuration
from home.models import get_recordings


def home(request):
    return render(request, 'home.html')


def recordings(request):
    return render(request, 'recordings.html', {"recordings": get_recordings()})


def watch(request, file_name):
    return render(request, 'watch.html', {"recordings": get_recordings(),
                                          "file_name": file_name})


def get_config(request):
    return render(request, 'configuration.html', {"config": Configuration.objects.first()})
