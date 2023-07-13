import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

client_id = "578feaebb8124668a3a166ad01842756"
client_secret = "359c2b4a7fef41cf825e712028f4d8e7"
redirect_uri = "https://9518-139-255-213-74.ngrok-free.app"
scope = "user-read-currently-playing, user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

def current_track(event, context):
    # Get the currently playing track
    current_track = sp.current_user_playing_track()

    # Check if a track is currently playing
    if current_track is None:
        response = {
            "statusCode": 200,
            "body": json.dumps({"message": "No track is currently playing."})
        }
    else:
        track_name = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        track_duration = current_track['item']['duration_ms']
        duration = time_format(track_duration)
        
        response = {
            "statusCode": 200,
            "body": json.dumps({"message": f"Currently playing: {track_name} - {artist_name} - {duration}"})
        }
    
    return response

def time_format(track_duration):
    seconds = track_duration // 1000
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    time_format = f"{minutes}:{remaining_seconds:02}"
    return time_format
