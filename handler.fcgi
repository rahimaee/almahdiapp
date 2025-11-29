#!/usr/bin/env python
import os
import sys

# مسیر پروژه را اضافه کن
sys.path.insert(0, r"D:\almahdi")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "almahdi_project.settings")

from flup.server.fcgi import WSGIServer
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

if __name__ == "__main__":
    WSGIServer(application).run()
