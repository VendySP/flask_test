import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask

app = Flask(__name__)

client_id = "578feaebb8124668a3a166ad01842756"
client_secret = "359c2b4a7fef41cf825e712028f4d8e7"
redirect_uri = "http://127.0.0.1:5000"
scope = "user-read-currently-playing user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

def time_format(track_duration):
    seconds = track_duration // 1000
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    time_format = f"{minutes}:{remaining_seconds:02}"
    return time_format

def current_track():
    # Get the currently playing track
    current_track = sp.current_user_playing_track()

    # Check if a track is currently playing
    if current_track is None:
        response_body = "No track is currently playing."
    else:
        track_name = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        track_duration = current_track['item']['duration_ms']
        duration = time_format(track_duration)
        
        response_body = f"Currently playing: {track_name} - {artist_name} - {duration}"

    # Return the response body
    return response_body

@app.route("/")
def index():
    response_body = current_track()
    return response_body, 200, {"Content-Type": "text/plain"}

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route("/execute_action/<action>", methods=["GET"])
def execute_action(action):
    if action == "resume_track":
        sp.start_playback()
        return "The track is resumed"
    elif action == "pause_track":
        sp.pause_playback()
        return "The track is paused"
    elif action == "next_track":
        sp.next_track()
        return "The track is skipped"
    elif action == "previous_track":
        sp.previous_track()
        return "Played previous track"
    else:
        return "Invalid action"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
