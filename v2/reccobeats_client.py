import requests

BASE_URL = "https://api.reccobeats.com/v1/audio-features"

def get_audio_features(track_ids):
    ids_string = ",".join(track_ids)

    try:
        response = requests.get(BASE_URL, params={"ids":ids_string})
        response.raise_for_status()
        return {
            "success": True,
            "data": response.json(),
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }
