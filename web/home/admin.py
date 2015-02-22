from django.contrib import admin

# Register your models here.
from models import Motion
from models import Recording

admin.site.register(Motion)
admin.site.register(Recording)
