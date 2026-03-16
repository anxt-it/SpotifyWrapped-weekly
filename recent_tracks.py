from spotify_client import results

recent_tracks = []

try:
    for item in results["items"]:

        track = item["track"]
        artists = track["artists"]

        artist_name = []
        artist_id = []

        for a in artists:
            artist_name.append(a["name"])
            artist_id.append(a["id"])

        recent_tracks.append(
            {
                "track_id" : track["id"],
                "track_name" : track["name"],
                "artist_id": "|".join(map(str, artist_id)),
                "artist_name": "|".join(map(str, artist_name)),
                "album_id": track["album"]["id"],
                "album_name": track["album"]["name"],
                "duration_ms": track["duration_ms"],
                "played_at": item["played_at"]
            }
        )

# temp
except KeyError as e: # e should be the missing key
    print(f"error {results["error"]["status"]}: {results["error"]["message"]}")
