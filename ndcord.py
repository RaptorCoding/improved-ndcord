import requests
from pypresence import Presence,ActivityType
import time, json

with open('secret.json') as f:
    secret_data = json.load(f)

client_id = secret_data.get('client_id', "")
server = secret_data.get('server', "")
username = secret_data.get('username', "")
password = secret_data.get('password', "")
label_name = secret_data.get('label_name', "")

RPC = Presence(client_id)
RPC.connect()

def get_now_playing_data(username, password):
    try:
        url = f"{server}rest/getNowPlaying.view?u={username}&p={password}&v=1.13.0&c=ndcord&f=json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        now_playing_entries = data.get("subsonic-response", {}).get("nowPlaying", {}).get("entry", [])
        for entry in now_playing_entries:
            if entry.get("username") == username:
                return entry

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")

    return None



def update_presence(username):
    now_playing_data = get_now_playing_data(username, password)

    if now_playing_data:
        title = now_playing_data.get("title", "")
        artist = now_playing_data.get("artist", "")
        album = now_playing_data.get("album", "")
        year = now_playing_data.get("year", "")
        album_id = now_playing_data.get("albumId", "")
        RPC.update(
            activity_type=ActivityType.LISTENING,
            state=f"By: {artist}",
            details=title,
            large_image= f"{server}rest/getCoverArt.view?u={username}&p={password}&v=1.16.0&c=ndcord&id={album_id}",
            large_text=f"{album} - {year}",
            # Remove this if you don't want to include the button
            buttons=[{
                "label": label_name,
                "url": f"{server}"
            }],
            ### End of the button
        )

try:
    while True:
        update_presence(username)
        time.sleep(15)
except KeyboardInterrupt:
    RPC.close()
    print("ndcord is terminated.")
