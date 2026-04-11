
def get_recent_tracks(results):
    recent_tracks = []


    for item in results["items"]:
        try:
            track = item["track"]
            artists = track["artists"]

            artist_name = []
            artist_id = []

            for a in artists:
                artist_name.append(a["name"])
                artist_id.append(a["id"])

            recent_tracks.append(
                {
                    "track_id": track["id"],
                    "track_name": track["name"],
                    "artist_id": "|".join(artist_id),
                    "artist_name": "|".join(artist_name),
                    "album_id": track["album"]["id"],
                    "album_name": track["album"]["name"],
                    "duration_ms": track["duration_ms"],
                    "played_at": item["played_at"]
                }
            )
        except (ValueError, KeyError):
            continue # skips the whole record

    return recent_tracks

