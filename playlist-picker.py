# where i come from, this script is called with a keybind
# i press Super+p and the rest gets handled
# the rest being an opened fzf window
# aregeuested user choice
# and an api request that plays the given playlist on the active player
# NOTE: if no player currently plays anything the request fails
# this is not yet fixed

import os
import sys
import subprocess
import requests
from get_token import get_access_token

PLAYLISTS_DIR = os.getenv("PLAYLISTS_FOLDER")

def refresh_playlists():
    token = get_access_token()
    os.makedirs(PLAYLISTS_DIR, exist_ok=True)

    url = "https://api.spotify.com/v1/me/playlists"
    while url:
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            params={"limit": 50}
        ).json()

        for item in response["items"]:
            safe_name = item["name"].replace('/', " - ")
            print(item["name"], safe_name)
            filepath = os.path.join(PLAYLISTS_DIR, safe_name)
            with open(filepath, "w") as f:
                f.write(item["id"])

        url = response.get("next")

    print("Playlists refreshed.")

def pick_playlist():
    result = subprocess.run(
        ["fzf"],
        input="\n".join(os.listdir(PLAYLISTS_DIR)),
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        sys.exit(0)

    chosen = result.stdout.strip()
    filepath = os.path.join(PLAYLISTS_DIR, chosen)
    with open(filepath) as f:
        return f.read().strip()

def play_playlist(playlist_id):
    token = get_access_token()
    response = requests.put(
        "https://api.spotify.com/v1/me/player/play",
        headers={"Authorization": f"Bearer {token}"},
        json={"context_uri": f"spotify:playlist:{playlist_id}"}
    )
    return response.status_code

if __name__ == "__main__":
    if "--refresh" in sys.argv:
        refresh_playlists()

    playlist_id = pick_playlist()
    play_playlist(playlist_id)

