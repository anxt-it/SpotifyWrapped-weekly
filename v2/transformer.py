
audio_features = ["acousticness","danceability","energy","instrumentalness","key","liveness","loudness","mode","tempo","valence"]

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
        for a in audio_features:
            features_dict[a] = item.get(a)

        results[track_id] = features_dict

    return results



def get_tables_results(spotify_json, audio_features_dict):
     albums_list = []
     artists_list = []
     plays_list = []
     tracks_artists = []
     tracks = []

     for item in spotify_json["items"]:
         track = item["track"]
         track_id = track["id"]

         album = track["album"]
         album_id = album["id"]

         artists = track["artists"]

         # create Artists table results
         for a in artists:
             artists_list.append(
                 {
                     "artist_id": a["id"],
                     "artist_name": a["name"]

                 }
             )

             # create Tracks_Artists table results
             tracks_artists.append(
                 {
                     "track_id": track_id,
                     "artist_id": a["id"]
                 }
             )


         # create Albums table results
         albums_list.append(
             {
                 "album_id":album_id,
                 "album_name":album["name"],
                 "album_type": album["type"],
                 "release_date": album["release_date"],
                 "album_image": album["images"][1]
             }
         )

         # create Plays table results
         plays_list.append(
            {
                "track_id": track_id,
                "played_at": item["played_at"]
            }
         )

         # create Tracks table results
         track_row = {
                 "track_id": track_id,
                 "track_name": track["name"],
                 "album_id": album_id,
                 "duration_ms": track["duration_ms"]
             }

         if track_id in audio_features_dict:
             for feature in audio_features:
                 track_row[feature] = audio_features_dict[track_id][feature]

         tracks.append(track_row)


     return {
         "Albums":albums_list,
         "Artists":artists_list,
         "Tracks":tracks,
         "Tracks_Artists":tracks_artists,
         "Plays":plays_list
     }
