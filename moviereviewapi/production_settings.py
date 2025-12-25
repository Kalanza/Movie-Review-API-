"""
Production settings for PythonAnywhere deployment
"""
from .settings import *
import os
from decouple import config

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
STATIC_ROOT = '/home/Kalanzaa/Movie-Review-API-/staticfiles'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/Kalanzaa/Movie-Review-API-/media'

# Database configuration (SQLite is fine for small projects)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/Kalanzaa/Movie-Review-API-/db.sqlite3',
    }
}

# Secret key from environment variable (REQUIRED - no fallback for security)
SECRET_KEY = config('SECRET_KEY')

# OMDB API Key from environment variable (REQUIRED - no fallback for security)
OMDB_API_KEY = config('OMDB_API_KEY')

