from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


PARENT_DIR = os.path.dirname(os.getcwd())
load_dotenv(os.path.join(PARENT_DIR, ".env"))

SCOPE = "user-read-recently-played"

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=SCOPE,
    cache_path=os.path.join(PARENT_DIR, ".cache")
))

def fetch_recent_tracks(limit=50):
    try:
        data = sp.current_user_recently_played(limit=limit)
        return {
        "success": True,
        "data": data,
        "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


