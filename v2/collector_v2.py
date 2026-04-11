import reccobeats_client, transformer, database_manager, spotify_client
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MANUAL_LOG_PATH = os.path.join(BASE_DIR, "collector_log.txt")


def log_locally(message):
    with open(MANUAL_LOG_PATH, "a") as file:
        file.write(message + '\n')

def init_event(log_row):
    insert_logs_results = database_manager.insert_logs(log_row)

    if not insert_logs_results["success"]:
        log_locally(message=f"{insert_logs_results['id']} || DB INSERT FAILED: {insert_logs_results['error']}")
        return None

    return insert_logs_results["id"]


def main():
    spotify_status = rb_status = db_status = "STARTED"
    spotify_message = rb_message = db_message = None

    current_log_id = init_event((spotify_status, spotify_message, rb_status, rb_message, db_status, db_message))

    if current_log_id is None:
        sys.exit()

    spotify_raw_results = spotify_client.fetch_recent_tracks(limit=40)

    if not spotify_raw_results["success"]:
        spotify_status = "FAILED"
        spotify_message = spotify_raw_results["error"]
        rb_status = "SKIPPED"
        rb_message = "Dependency failed: Spotify error"
        update_result_s = database_manager.update_logs(current_log_id, (spotify_status, spotify_message, rb_status, rb_message, db_status, db_message))
        if not update_result_s["success"]:
            log_locally(f"SPOTIFY FAIL. DB UPDATE FAILED FOR {current_log_id}. Error: {update_result_s['error']}")
        sys.exit()

    spotify_status = "SUCCESS"

    tracks_set = transformer.get_tracks_set(spotify_raw_results["data"]) # gets unique track ids

    rb_raw_results = reccobeats_client.get_audio_features(tracks_set) # get results from reccobeatss

    if rb_raw_results["success"]:
        rb_status = "SUCCESS"
        reccobeats_dict = transformer.get_reccobeats_results(rb_raw_results["data"])

    else:
        rb_status = "FAILED"
        rb_message = rb_raw_results["error"]
        reccobeats_dict = {}

    # transformer
    tables_dict = transformer.get_tables_results(spotify_raw_results["data"], reccobeats_dict)
    for row in tables_dict["Plays"]:
        row.append(current_log_id)

    # db managerlog
    insert_results = database_manager.insert(tables_dict)
    if not insert_results["success"]:
        db_status = "FAILED"
        db_message = insert_results["error"]

    else:
        db_status = "SUCCESS"

    update_result_db = database_manager.update_logs(current_log_id, (spotify_status, spotify_message, rb_status, rb_message, db_status, db_message))
    if not update_result_db["success"]:
        log_locally(f"DB FAIL. DB UPDATE FAIL FOR {current_log_id}. ERROR: {update_result_db['error']}")

if __name__ == "__main__":
    main()





