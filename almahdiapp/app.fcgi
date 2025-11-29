#!/usr/bin/env python
import os
from flup.server.fcgi import WSGIServer
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
application = get_wsgi_application()

if __name__ == "__main__":
    WSGIServer(application).run()
