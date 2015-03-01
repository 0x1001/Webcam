#!/usr/bin/env python
import os
import sys
from gevent import monkey

if __name__ == "__main__":
    monkey.patch_all()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webcam.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
