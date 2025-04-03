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
    print(f"Device found: {devices['devices'][0]['name']}")

    # Get song name from user input
    song_name = input("Enter the song name you want to play: ")

    # Search for the song on Spotify
    results = sp.search(q=song_name, type='track', limit=1)

    if results['tracks']['items']:
        # Get the URI of the first search result (the best match)
        song_uri = results['tracks']['items'][0]['uri']
        song_title = results['tracks']['items'][0]['name']
        artist = results['tracks']['items'][0]['artists'][0]['name']

        print(f"Playing: {song_title} by {artist}")

        # Start playback on the chosen device
        sp.start_playback(device_id=device_id, uris=[song_uri])

        print("Song is now playing!")
    else:
        print("No song found with that name. Please try again.")

