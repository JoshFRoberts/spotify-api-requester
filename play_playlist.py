import sys
import requests
from get_token import get_access_token

def play_playlist(playlist_id):
    token = get_access_token()
    response = requests.put(
        "https://api.spotify.com/v1/me/player/play",
        headers={"Authorization": f"Bearer {token}"},
        json={"context_uri": f"spotify:playlist:{playlist_id}"}
    )
    response.raise_for_satus()

    return response.status_code

if __name__ == "__main__":
    playlist_id = sys.stdin.read().strip()
    status = play_playlist(playlist_id)
    print(f"Status: {status}")
