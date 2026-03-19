import sqlite3

# make the request
from spotify_client import sp_results as raw_results
from recent_tracks import get_recent_tracks

from clean_recent_tracks import load_df, clean_data_frame


# get extracted data
if "error" in raw_results:
    raise RuntimeError(f"Spotify API error {raw_results["error"]["status"]}: {raw_results["error"]["message"]}")

records = get_recent_tracks(raw_results)

# clean the data
df = load_df(records)
cleaned_df = clean_data_frame(df)

# write dataframe to sqlite
TEST_FILE_DB = 'spotify_test.db'

conn = sqlite3.connect(TEST_FILE_DB)
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

cursor.execute(create_table_query) # execute the sql command


insert_or_ignore_query = """
    INSERT OR IGNORE INTO listening_history
    (track_id, track_name, artist_id, artist_name, album_id, album_name, duration_ms, played_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

cursor.executemany(insert_or_ignore_query, cleaned_df)

conn.commit() # commit the changes
conn.close()

