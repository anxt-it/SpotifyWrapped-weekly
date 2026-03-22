# 🎧 Spotify Weekly Wrapped 

A Python-based data pipeline that tracks your Spotify listening habits and sends a personalized "Weekly Wrapped" report to your email every Saturday.

**Current version: v1 (MVP)**

The focus of v1 was building a reliable, fully automated pipeline with clean seperation between extraction, transformation, loading, and reporting. 

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


## Future Roadmap: Version 2.0 || In Progress 
Currently rearchitecting the system to handle deeper analytics and a more scalable data model.
- **Relational Schema:** Moving from a flat table to a normalized database (Tracks, Artists, Albums, and Plays) to handle many-to-many relationships.
- **Audio Feature Integration:** Incorporating track metadata like `energy`, `danceability`, and `valence` for mood based analysis.
- **Frontend Dashboard:** Transitioning from static emails to a dynamic **React** dashboard for real-time data visualization.


## Setup
1. Clone the repository.
2. Create a `.env` file with your Spotify and SMTP credentials.
3. Install dependencies: `pip install -r requirements.txt`
4. Set up Cron jobs for hourly collection and weekly reporting.
