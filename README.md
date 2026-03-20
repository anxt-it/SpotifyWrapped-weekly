# 🎧 Spotify Weekly Wrapped (Automated)

A Python-based data pipeline that tracks your Spotify listening habits and sends a personalized "Weekly Wrapped" report to your email every Saturday.

## Features
- **Automated Collection:** Runs hourly via Cron to fetch recently played tracks.
- **SQLite database storage:** Uses SQLite with `INSERT OR IGNORE` logic to prevent duplicate entries.
- **SQL Analytics:** Analysis is decoupled from Python logic using external `.sql` query files.
- **Email Reporting:** Generates and sends a stylized HTML email with top artists, songs, and total listening time.

## Project Structure
- `spotify_client.py`: Centralized Spotify API authentication.
- `recent_tracks.py`: Helper module that parses the raw, nested JSON from Spotify's API into a clean python dictionary.
- `collector.py`: Handles API extraction and database loading.
- `wrapped_queries.sql`: Contains the analytical SQL logic for the weekly reports.
- `reporter.py`: Parses SQL queries, builds HTML, and sends emails.

## Tech Stack
- **Language:** Python 3.x
- **API:** Spotipy (Spotify Web API)
- **Database:** SQLite
- **Automation:** Cron
- **Infrastructure:** `python-dotenv` for secret management, `smtplib` for email delivery, `spotipy` for spotify's API

## Setup
1. Clone the repository.
2. Create a `.env` file with your Spotify and SMTP credentials.
3. Install dependencies: `pip install -r requirements.txt`
4. Set up Cron jobs for hourly collection and weekly reporting.
