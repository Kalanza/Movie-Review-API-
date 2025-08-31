import requests
from django.conf import settings

OMDB_API_KEY = getattr(settings, 'OMDB_API_KEY', None)
OMDB_API_URL = 'http://www.omdbapi.com/'

def fetch_movie_info(title):
    if not OMDB_API_KEY:
        return None
    params = {
        't': title,
        'apikey': OMDB_API_KEY
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
