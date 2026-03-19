import sqlite3

# make the request
from spotify_client import fetch_recent_tracks
from recent_tracks import get_recent_tracks

def run_pipeline():

    # extraction
    raw_results = fetch_recent_tracks(limit=3)

    if "error" in raw_results:
        raise RuntimeError(f"Spotify API error {raw_results["error"]["status"]}: {raw_results["error"]["message"]}")

    records = get_recent_tracks(raw_results)


    # load
    data_to_insert = [
        (r['track_id'], r['track_name'], r['artist_id'], r['artist_name'],
         r['album_id'], r['album_name'], r['duration_ms'], r['played_at'])
        for r in records
    ]

    with sqlite3.connect('spotify_test.db') as conn:
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS listening_history (
            track_id TEXT,  
            track_name TEXT,
            artist_id TEXT,
            artist_name TEXT,
            album_id TEXT,
            album_name TEXT,
            duration_ms INT, 
            played_at DATETIME,
            UNIQUE (played_at)

        );
        """

        cursor.execute(create_table_query)

        cursor.executemany(
            "INSERT OR IGNORE INTO listening_history VALUES (?,?,?,?,?,?,?,?)",
            data_to_insert
        )
        print(f"Done. Check your DB, we just processed {len(data_to_insert)} tracks.")

if __name__ == "__main__":
    run_pipeline()
