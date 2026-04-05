import sqlite3
import os
import re

# create a create_tables_query dict
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'spotify_v2_test.db')

# initialize db
def init_db():
    init_queries ={
    "Plays": """
    CREATE TABLE IF NOT EXISTS Plays (
        track_id TEXT,
        played_at TEXT UNIQUE, 
        exrtaction_id INT
    )
    """,
    "Tracks": """
    CREATE TABLE IF NOT EXISTS Tracks (
        track_id TEXT PRIMARY KEY,
        track_name TEXT,
        album_id TEXT,
        duration_ms INT,
        acousticness FLOAT,
        danceability FLOAT,
        energy FLOAT,
        instrumental FLOAT,
        key INT, 
        liveness FLOAT,
        loudness FLOAT,
        mode INT, 
        tempo FLOAT,
        valence FLOAT
    )
    """,
    "Albums": """
    CREATE TABLE IF NOT EXISTS Albums (
        album_id TEXT PRIMARY KEY, 
        album_name TEXT, 
        album_artist_id TEXT, 
        album_image TEXT
    )
    """,
    "Artists": """
    CREATE TABLE IF NOT EXISTS Artists (
        artist_id TEXT PRIMARY KEY, 
        artist_name TEXT,
        artist_image TEXT
    )
    """,
    "Track_Artists": """
    CREATE TABLE IF NOT EXISTS Track_Artists (
        track_id TEXT,
        artist_id TEXT
    )
    """
    # "Extraction_log": """
    # CREATE TABLE IF NOT EXISTS Extraction_log (
    #     extracted_at DATETIME,
    #     log TEXT
    # )
    # """
}

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        for query in init_queries.values():
            cursor.execute(query)


# insert or ignore new data into tables
def insert(data_dict):
    insert_ignore_queries = {
         "Albums": """
         INSERT OR IGNORE INTO Albums (
         album_id, album_name, album_artist_id, album_image
         ) VALUES (?,?,?,?) 
         """,
         "Artists": """
        INSERT OR IGNORE INTO Artists (
         artist_id, artist_name, artist_image
         ) VALUES (?,?,?) 
         """,
         "Tracks": """
         INSERT OR IGNORE INTO Tracks 
         (track_id, track_name, album_id, duration_ms, acousticness, danceability, energy, instrumental, key, liveness,loudness,mode, tempo, valence)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
         """,
         "Track_Artists": """
         INSERT OR IGNORE INTO Track_Artists (track_id, artist_id) VALUES (?,?)
         """,
         "Plays":"""
         INSERT OR IGNORE INTO Plays (track_id, played_at) VALUES (?,?)
         """
     }

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            for table in insert_ignore_queries:
                query = insert_ignore_queries[table]
                data_to_insert = data_dict.get(table, []) # this is a list with x values (x rows)
                cursor.executemany(query, data_to_insert)

    except Exception as e:
        print("[DB ERROR]", e)
        raise


# handle the queries for the reporter
def create_queries_dict(queries_file):
    with open(queries_file, 'r') as file:
        content = file.read()

    pattern = r"--\s*name:\s*(\w+)\s*\n(.*?)(?=(?:--\s*name:|$))"

    matches = re.findall(pattern, content, re.DOTALL)

    queries_dict = dict()

    for match in matches:
        queries_dict[match[0]] = match[1]

    return queries_dict

def exec_query(sql_query):
    with sqlite3.connect(os.path.join(BASE_DIR, 'spotify_listening_history.db')) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_query)

    rows = cursor.fetchall()
    return rows