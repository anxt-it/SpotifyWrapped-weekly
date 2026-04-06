
AUDIO_FEATURES = ["acousticness", "danceability", "energy", "instrumentalness", "key", "liveness", "loudness", "mode", "tempo", "valence"]

def get_tracks_set(spotify_json):
    track_ids = set()
    for item in spotify_json["items"]:
        track_ids.add(item["track"]["id"])

    return track_ids

def get_reccobeats_results(reccobeats_json):
    results = {}

    for item in reccobeats_json["content"]:

        track_id = item["href"].split('/')[-1] # gets track_id like in spotify

        features_dict = {}
        for a in AUDIO_FEATURES:
            features_dict[a] = item.get(a)

        results[track_id] = features_dict

    return results


def get_tables_results(spotify_json, audio_features_dict):
    albums_list = []
    artists_list = []
    plays_list = []
    tracks_artists_list = []
    albums_artists_list = []
    tracks_list = []

    for item in spotify_json["items"]:
        track = item["track"]
        track_id = track["id"]

        album = track["album"]
        album_id = album["id"]

        artists = track["artists"]


        # create Artists table results
        for a in artists:
            artists_list.append(
                (a["id"], a["name"]) # artist_id, artist_name
            )

            # create Tracks_Artists table results
            tracks_artists_list.append(
                (track_id, a["id"]) # track_id, artist_id
            )


        # create Albums table results
        albums_list.append(
            (album_id, album["name"], album["type"], album["release_date"], album["images"][1]["url"])
        )

        # create Albums_Artists table results
        for artist in album["artists"]:
            albums_artists_list.append(
                (album_id, artist["id"]) # album_id, album_artists_id
            )


        # create Plays table results
        plays_list.append(
            (track_id, item["played_at"]) # track_id, played_at
        )

        # create Tracks table results
        track_row = [
            track_id,
            track["name"],
            album_id,
            track["duration_ms"]
        ]


        if track_id in audio_features_dict:
            for feature in AUDIO_FEATURES:
                track_row.append(audio_features_dict[track_id][feature])
        else:
            for _ in range(len(AUDIO_FEATURES)):
                track_row.append(None)

        tracks_list.append(tuple(track_row))

    return {
        "Albums": albums_list,
        "Artists": artists_list,
        "Tracks": tracks_list,
        "Tracks_Artists": tracks_artists_list,
        "Albums_Artists": albums_artists_list,
        "Plays": plays_list
    }
