import requests

BASE_URL = "https://api.reccobeats.com/v1/audio-features"

def get_audio_features(track_ids):
    ids_string = ",".join(track_ids)

    try:
        response = requests.get(BASE_URL, params={"ids":ids_string})
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f'ReccoBeats API Error: {e}')
        return []
