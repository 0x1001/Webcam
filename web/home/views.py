from django.shortcuts import render
from home.models import Recording
from home.models import Configuration


def home(request):
    return render(request, 'home.html')


def recordings(request):
    return render(request, 'recordings.html', {"recordings": Recording.objects.all()})


def watch(request, file_name):
    return render(request, 'watch.html', {"recordings": Recording.objects.all(),
                                          "file_name": file_name})


def get_config(request):
    return render(request, 'configuration.html', {"config": Configuration.objects.first()})
