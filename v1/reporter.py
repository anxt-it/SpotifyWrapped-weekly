import re
import sqlite3
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from datetime import datetime, UTC


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
load_dotenv(os.path.join(PARENT_DIR, ".env"))


EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")



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


def build_top_artists_table(top_artist_results):
    rows = ''
    for artist, count in top_artist_results:
        rows += f"""
        <tr>
            <td>{artist}</td>
            <td>{count}</td>
        </tr>
        """

    return f"""
    <h2>Your Top five artists were</h2>
    <table style="width: 100%">
        <tr>
            <th>Artist</th>
            <th>Number of songs played</th>
        </tr>
        {rows}
    </table>
    """

def build_top_songs_section(top_songs_results):
    rows = ''
    for track, artist, count in top_songs_results:
        rows += f"<p>You listened to {track} by {artist}, {count} times this week.</p>"

    return f"""
    <h2>Your Top 10 songs were</h2>
    {rows}
    """

def build_total_time_section(total_time_results):
    time = 'minutes'
    if total_time_results > 60:
        total_time_results = total_time_results / 60
        time = 'hours'

    return f"<h3>This week you spent {total_time_results} {time} with your music.</h3>"


def format_results_to_html(total_time, top_artist, top_songs):
    total_time_html = build_total_time_section(total_time)
    artists_html = build_top_artists_table(top_artist)
    songs_html = build_top_songs_section(top_songs)

    return f"""
    <html>
    <style>
    table, th, td {{
        border:1px solid black;
    }}
    </style>

    <body>

        <h1>Weekly Spotify Wrapped</h1>

        {total_time_html}
        {artists_html}
        {songs_html}

    </body>
    </html>
    """


def send_email(html_content):
    msg = EmailMessage()
    msg['Subject'] = "Weekly Spotify Wrapped"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT)) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"[REPORTER] {datetime.now(UTC).isoformat()}")


def run_report():
    queries = create_queries_dict(os.path.join(BASE_DIR, 'wrapped_queries.sql'))

    results = exec_query(queries['total_time'])
    total_time = results[0][0] if results and results[0][0] is not None else 0

    top_artists = exec_query(queries['top_five_artists'])
    top_songs = exec_query(queries['top_ten_songs'])

    html = format_results_to_html(total_time, top_artists, top_songs)

    send_email(html)


if __name__ == "__main__":
    run_report()