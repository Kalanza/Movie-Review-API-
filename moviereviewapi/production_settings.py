"""
Production settings for PythonAnywhere deployment
"""
from .settings import *
import os

# Production settings
DEBUG = False

# Update allowed hosts for PythonAnywhere
ALLOWED_HOSTS = ['kalanzaa.pythonanywhere.com', 'www.kalanzaa.pythonanywhere.com']

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files configuration for PythonAnywhere
STATIC_URL = '/static/'
STATIC_ROOT = '/home/kalanzaa/Movie-Review-API-/static'

# Database configuration (SQLite is fine for small projects)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/kalanzaa/Movie-Review-API-/db.sqlite3',
    }
}

# Secret key from environment variable
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-!vm4=%#ukw=(p#ttxlrm-+(x1sx2n5izw4*84^0qyqp-2=ur$=')

# OMDB API Key from environment variable
OMDB_API_KEY = os.environ.get('OMDB_API_KEY', 'YOUR_OMDB_API_KEY')
