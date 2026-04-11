import sqlite3
import os
import re
from datetime import datetime, UTC

# create a create_tables_query dict
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'spotify_v2_test.db')


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
    with sqlite3.connect(os.path.join(BASE_DIR, 'spotify_v2_test.db')) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_query)

    rows = cursor.fetchall()
    return rows


# initialize db
def init_db():
    init_queries ={
    "Plays": """
    CREATE TABLE IF NOT EXISTS Plays (
        track_id TEXT PRIMARY KEY,
        played_at TEXT UNIQUE, 
        log_id INT,
        FOREIGN KEY (track_id) REFERENCES Tracks(track_id)
        FOREIGN KEY (log_id) REFERENCES Logs(log_id)
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
        valence FLOAT,
        FOREIGN KEY (album_id) REFERENCES Albums(album_id)
    )
    """,
    "Albums": """
    CREATE TABLE IF NOT EXISTS Albums (
        album_id TEXT PRIMARY KEY, 
        album_name TEXT, 
        album_type TEXT,
        album_release_date DATETIME,
        album_image TEXT
    )
    """,
    "Artists": """
    CREATE TABLE IF NOT EXISTS Artists (
        artist_id TEXT PRIMARY KEY, 
        artist_name TEXT
    )
    """,
    "Tracks_Artists": """
    CREATE TABLE IF NOT EXISTS Tracks_Artists (
        track_id TEXT,
        artist_id TEXT,
        PRIMARY KEY (track_id, artist_id),
        FOREIGN KEY (track_id) REFERENCES Tracks(track_id),
        FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
        
    )
    """,
    "Albums_Artists": """
    CREATE TABLE IF NOT EXISTS Albums_Artists (
        album_id TEXT,
        artist_id TEXT,
        PRIMARY KEY (album_id, artist_id),
        FOREIGN KEY (album_id) REFERENCES Albums(album_id),
        FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
    )
    """,
    "Logs": """
    CREATE TABLE IF NOT EXISTS Logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        extraction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        spotify_status TEXT,
        spotify_error TEXT, 
        reccobeats_status TEXT,
        reccobeats_error TEXT,
        db_status TEXT,
        db_error TEXT
    )
    """
}

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")

        for query in init_queries.values():
            cursor.execute(query)


# insert new data into tables
def insert(data_dict):
    insert_ignore_queries = {
         "Albums": """
         INSERT OR IGNORE INTO Albums (
         album_id, album_name, album_type, album_release_date, album_image
         ) VALUES (?,?,?,?,?) 
         """,
         "Artists": """
        INSERT OR IGNORE INTO Artists (
         artist_id, artist_name
         ) VALUES (?,?) 
         """,
         "Tracks_Artists": """
         INSERT OR IGNORE INTO Tracks_Artists (track_id, artist_id) VALUES (?,?)
         """,
        "Albums_Artists": """
                         INSERT
                         OR IGNORE INTO Albums_Artists (album_id, artist_id) VALUES (?,?)
                         """,
         "Plays":"""
         INSERT OR IGNORE INTO Plays (track_id, played_at, log_id) VALUES (?,?,?)
         """,
         "Tracks": """
         INSERT OR IGNORE INTO Tracks 
         (track_id, track_name, album_id, duration_ms, acousticness, danceability, energy, instrumental, key, liveness,loudness,mode, tempo, valence)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
         """
     }
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            for table in insert_ignore_queries:

                query = insert_ignore_queries[table]
                data_to_insert = data_dict.get(table, [])

                cursor.executemany(query, data_to_insert)

        return {
            "success": True,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# insert the logs
def insert_logs(logs_to_insert):
   try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            query = """
            INSERT OR IGNORE INTO Logs 
            (spotify_status, spotify_error, reccobeats_status, reccobeats_error, db_status, db_error)
            VALUES (?,?,?,?,?,?)
            """

            cursor.execute(query, logs_to_insert)
        return {
            "success": True,
            "error": None,
            "id": cursor.lastrowid
        }

   except Exception as e:
       return {
           "success": False,
           "error": str(e),
           "id": datetime.now(UTC).isoformat()
       }


def update_logs(log_id, log_row):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            query = """
            UPDATE Logs
            SET spotify_status = ?, spotify_error = ?, reccobeats_status = ?, reccobeats_error = ?, db_status = ?, db_error = ?
            WHERE id = ?
            """
            cursor.execute(query, (*log_row, log_id))
        return {
            "success": True,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
