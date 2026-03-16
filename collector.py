
# make the request
from spotify_client import sp_results
from recent_tracks import get_recent_tracks

# get extracted data
if "error" in sp_results:
    raise RuntimeError(f"Spotify API error {sp_results["error"]["status"]}: {sp_results["error"]["message"]}")

uncleaned_data = get_recent_tracks(sp_results)


# clean the data - call clean_recent_tracks


# show it to me