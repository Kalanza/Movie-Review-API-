import requests
from django.conf import settings

OMDB_API_KEY = getattr(settings, 'OMDB_API_KEY', None)
OMDB_API_URL = 'http://www.omdbapi.com/'

def fetch_movie_info(title):
    """
    Fetch movie information by title from OMDB API
    """
    if not OMDB_API_KEY:
        return None
    params = {
        't': title,
        'apikey': OMDB_API_KEY,
        'plot': 'full'
    }
    try:
        response = requests.get(OMDB_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                return data
    except Exception:
        pass
    return None

def search_movies(search_term):
    """
    Search for movies by term from OMDB API
    """
    if not OMDB_API_KEY:
        return None
    params = {
        's': search_term,
        'apikey': OMDB_API_KEY,
        'type': 'movie'
    }
    try:
        response = requests.get(OMDB_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                return data.get('Search', [])
    except Exception:
        pass
    return None

def fetch_movie_by_imdb_id(imdb_id):
    """
    Fetch movie information by IMDB ID from OMDB API
    """
    if not OMDB_API_KEY:
        return None
    params = {
        'i': imdb_id,
        'apikey': OMDB_API_KEY,
        'plot': 'full'
    }
    try:
        response = requests.get(OMDB_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                return data
    except Exception:
        pass
    return None
