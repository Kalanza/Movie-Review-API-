"""
WSGI config for moviereviewapi project for PythonAnywhere.
"""

import os
import sys

# Add your project directory to sys.path
path = '/home/Kalanzaa/Movie-Review-API-'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviereviewapi.production_settings')
os.environ.setdefault('OMDB_API_KEY', '6daeffea')
os.environ.setdefault('DJANGO_SECRET_KEY', '1e978399a168fb7a33a7f781992e0640183a4068')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
