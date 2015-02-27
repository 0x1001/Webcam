from django.contrib import admin

# Register your models here.
from models import Movement
from models import Recording

admin.site.register(Movement)
admin.site.register(Recording)
