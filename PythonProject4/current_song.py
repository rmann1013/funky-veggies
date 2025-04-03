import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify credentials (Replace these with your own credentials)
CLIENT_ID = "3266596fe0fa43aa83b0b30ca77b23a6"
CLIENT_SECRET = "69f5364ec0fa4c8089d73d7fa829b8d2"
REDIRECT_URI = 'http://127.0.0.1:8080/callback'
SCOPE = "user-library-read user-read-playback-state user-modify-playback-state"

# Authenticate using SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

# Get the current playback device
devices = sp.devices()

# Check if there are any available devices
if not devices['devices']:
    print("No active devices found. Please make sure your Spotify client is running and connected.")
else:
    # Get the first available device
    device_id = devices['devices'][0]['id']
    #print(f"Device found: {devices['devices'][0]['name']}")

    # Get the currently playing track
    current_playback = sp.current_playback()

    if current_playback and current_playback.get('item'):
        # Get the title and artist of the currently playing song
        song_title = current_playback['item']['name']
        artist = current_playback['item']['artists'][0]['name']
        song_id = current_playback['item']['id']

        print(f"Currently playing: {song_title} by {artist}")
        print(f"Song ID: {song_id}")
    else:
        print("No song is currently playing.")
