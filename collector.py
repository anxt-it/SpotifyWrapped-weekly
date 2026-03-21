import datetime
import sqlite3
import os
from datetime import datetime, UTC

from spotify_client import fetch_recent_tracks
from recent_tracks import get_recent_tracks

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'spotify_listening_history.db')

def run_pipeline():

    # extraction
    raw_results = fetch_recent_tracks(limit=50)

    if "error" in raw_results:
        raise RuntimeError(f"Spotify API error {raw_results["error"]["status"]}: {raw_results["error"]["message"]}")

    records = get_recent_tracks(raw_results)

    # load
    data_to_insert = [
        (r['track_id'], r['track_name'], r['artist_id'], r['artist_name'],
         r['album_id'], r['album_name'], r['duration_ms'], r['played_at'])
        for r in records
    ]

    with sqlite3.connect(DB_PATH) as conn:
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
            played_at DATETIME UNIQUE,
            extracted_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """

        cursor.execute(create_table_query)

        insert_or_ignore_query = """
                    INSERT OR IGNORE INTO listening_history 
                    (track_id, track_name, artist_id, artist_name, album_id, album_name, duration_ms, played_at) 
                    VALUES (?,?,?,?,?,?,?,?)
                    """

        cursor.executemany(insert_or_ignore_query, data_to_insert)

        # print(f"Done at {datetime.now(UTC)}. Processed {len(data_to_insert)} tracks.")
        print(f"[COLLECTOR] {datetime.now(UTC).isoformat()} | inserted={len(data_to_insert)}")

if __name__ == "__main__":
    run_pipeline()
