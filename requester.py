import argparse

import requests
import json

import get_token as token

class SpotifyAPIException(Exception):
    pass


class SpotifyConnection:
    def __init__(self):
        self.bearer_token = token.get_access_token()

    def notify_send(self, title, message):
        import subprocess
        import os

        # Set XDG_RUNTIME_DIR to the user's runtime directory
        user_id = os.getuid()
        runtime_dir = f"/run/user/{user_id}"

        # Set environment variables
        env = os.environ.copy()
        env["XDG_RUNTIME_DIR"] = runtime_dir
        env["DISPLAY"] = ":0"

        # Execute notify-send
        subprocess.run(
            ["notify-send", title, message],
            env=env,
            check=True
        )


    def get_artist(self, artist_id:str) -> dict:
        response = requests.get(
            'https://api.spotify.com/v1/artists' + f"/{artist_id}",
                headers={'Authorization': f'Bearer {self.bearer_token}'}
        )
        response.raise_for_status()

        return dict(response.json())

    def get_album(self, album_id:str) -> dict:
        response = requests.get(
            'https://api.spotify.com/v1/albums' + f'/{album_id}',
                 headers={
                     'Authorization': f'Bearer {self.bearer_token}',
                 })
        response.raise_for_status()

        return dict(response.json())

    def get_song(self, song_link:str):
        song_id: str = sys.argparse[1]
        response = requests.get(
            f'https://api.spotify.com/v1/tracks/{song_id}',
                headers={'Authorisation': f'Bearer {self.bearer_token}'},
                params={
                    'market': 'DE',
                    'fields': 'tracks'
                    }
            )

    def add_song_to_queue(self):
        import sys
        import pyperclip

        link = pyperclip.paste()

        # this picks only the track id out
        # of a spotify link someone sent per chat
        # without anything else of the url
        # no server address
        # no track id (especially no track id (we hate those))
        track_id = link.replace("https://open.spotify.com/track/", "").split("?")[0]

        response = requests.post(
            'https://api.spotify.com/v1/me/player/queue',
                headers={'Authorization': f'Bearer {self.bearer_token}'},
                params={'uri': f'spotify:track:{track_id}'}
            )
        self.notify_send("mistekiste", response.raise_for_status())


    def get_playlist(self, playlist_id:str) -> list:
        response = requests.get(
            f'https://api.spotify.com/v1/playlists/{playlist_id}',
                headers={'Authorization': f'Bearer {self.access_token}'},
                params={
                    'market': 'DE',
                    'fields': 'tracks.items(track(name, artists(name))'
                }
            )
        response.raise_for_status()

        tracks = response.json().get('tracks').get('items')
        returned_list: list[dict[str, str]] = []

        for track in tracks:
            song = track['track']['name']
            artists = track['track']['artists']
            artist_names: list[str] = []
            for artist in artists:
                artist_name = artist['name']
                artist_names.append(artist_name)

            returned_list.append({
                'name': song,
                'all_artists': artist_names,
            })

            print(f'{song['name']}: ', end='')
            for index, artist in enumerate(song['all_artists']):
                print(f'{artist}', end='')
                if not index == len(song['all_artists']) - 1:
                    print(', ', end='')
                print()

        return returned_list

    def search(self, key:str, value:str) -> dict:
        response = requests.get(
            'https://api.spotify.com/v1/search',
                headers={ 'Authorization': f'Bearer {self.client_id}'},
                params={
                    'q': f'{value}',
                    'type': f'{key}',
                    'market': 'DE',
                    'limit': '10',
                    'offset': '0'
                })
        response.raise_for_status()

        return dict(response.json())


if __name__ == '__main__':

    con = SpotifyConnection()

    # default_value = '0xfprdFzAdLVlSRvbskpd5'
    # replace default value with playlist id found in spotify link to playlist
    # maybe later on replace with full link and parse id to improve usability

    con.add_song_to_queue()
