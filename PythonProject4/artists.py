import requests
import base64

CLIENT_ID = "3266596fe0fa43aa83b0b30ca77b23a6"
CLIENT_SECRET = "69f5364ec0fa4c8089d73d7fa829b8d2"

def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(bytes(CLIENT_ID + ":" + CLIENT_SECRET, "utf-8")).decode("utf-8")
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]

def search_artist(artist_name, token):
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    artist_data = response.json()

    if artist_data["artists"]["items"]:
        artist = artist_data["artists"]["items"][0]
        return artist["id"], artist["name"]
    return None, None


# Function to get an artist's top tracks
def get_artist_top_tracks(artist_id, token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    tracks_data = response.json()

    return [track["name"] for track in tracks_data["tracks"]]


# Main execution
if __name__ == "__main__":
    token = get_access_token()
    artist_id, artist_name = search_artist("Taylor Swift", token)

    if artist_id:
        print(f"Top tracks of {artist_name}:")
        top_tracks = get_artist_top_tracks(artist_id, token)
        for i, track in enumerate(top_tracks, 1):
            print(f"{i}. {track}")
    else:
        print("Artist not found.")

    