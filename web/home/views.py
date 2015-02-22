from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def recordings(request):
    from home.models import Recording
    return render(request, 'recordings.html', {"recordings": Recording.objects.all()})


def watch(request, file_name):
    from home.models import Recording
    return render(request, 'watch.html', {"recordings": Recording.objects.all(),
                                          "file_name": file_name})