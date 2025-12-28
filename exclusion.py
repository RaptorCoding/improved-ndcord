import requests
import time, json
import csv
from pathlib import Path

with open('secret.json') as f:
    secret_data = json.load(f)

server = secret_data.get('server', "")
username = secret_data.get('username', "")
password = secret_data.get('password', "")
label_name = secret_data.get('label_name', "")
playlist_id = input("Enter Playlist ID (In URL between Playlist and Show):")
def getPlaylist_data(username, password):
    try:
        url = f"{server}rest/getPlaylist?u={username}&p={password}&v=1.16.0&c=ndcord-exclusions&id={playlist_id}&f=json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        playlist_entries = data.get("subsonic-response", {}).get("playlist", {}).get("entry", [])
        for entry in playlist_entries:
            song_id = entry.get("id", "")

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")

    return None

