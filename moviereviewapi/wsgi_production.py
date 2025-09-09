"""
WSGI config for moviereviewapi project for PythonAnywhere.
"""

import os
import sys

# Add your project directory to sys.path
path = '/home/Kalanzaa/Movie-Review-API-'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviereviewapi.production_settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
