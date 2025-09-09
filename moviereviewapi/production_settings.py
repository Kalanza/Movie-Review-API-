"""
Production settings for PythonAnywhere deployment
"""
from .settings import *
import os

# Production settings
DEBUG = False

# Update allowed hosts for PythonAnywhere
ALLOWED_HOSTS = ['Kalanzaa.pythonanywhere.com', 'www.Kalanzaa.pythonanywhere.com']

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files configuration for PythonAnywhere
STATIC_URL = '/static/'
STATIC_ROOT = '/home/Kalanzaa/Movie-Review-API-/static'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/Kalanzaa/Movie-Review-API-/media'

# Database configuration (SQLite is fine for small projects)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Secret key from environment variable
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-!vm4=%#ukw=(p#ttxlrm-+(x1sx2n5izw4*84^0qyqp-2=ur$=')

# OMDB API Key from environment variable
OMDB_API_KEY = os.environ.get('OMDB_API_KEY', 'eb694b1d')
