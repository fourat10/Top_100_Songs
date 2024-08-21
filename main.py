import requests
from bs4 import BeautifulSoup
import smtplib
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("donner date YYYY-MM-DD = ")

url = f"https://www.billboard.com/charts/hot-100/{date}/"
page = requests.get(url=url)

# SPOTIFY

client_id ="xxxx"
client_secret = "xxxx"
redirect_uri = "https://www.billboard.com/charts/hot-100/2018-01-01/"
scope = "playlist-modify-private playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_path=".cache",
))

# Get the current user's ID
user_id = sp.current_user()["id"]
print(f"User ID: {user_id}")

# Example: Get current user's playlists
playlists = sp.current_user_playlists()
for playlist in playlists['items']:
    print(playlist['name'])
src = page.content
soup = BeautifulSoup(src, "html.parser")
song_names=[]
for x in soup.select(".o-chart-results-list-row-container "):
    song_element = x.find(name="h3", id="title-of-a-story")
    if song_element:
        # Extract the text and strip it
        song_name = song_element.get_text(strip=True)
        song_names.append(song_name)#names = soup.find_all(name="h3" , id="title-of-a-story" ,class_="c-title" )

print((song_names))

print(date.split('-')[0])

def search_song(song_names):
    song_uris = []
    global date
    for song  in song_names :
        result = sp.search(q=f"track:{song} year:{date.split('-')[0]}", type="track")
        tracks = result['tracks']['items']
        if tracks:
            uri = tracks[0]["uri"]
            song_uris.append(uri)
        else:
            print(f"{song} doesn't exist in Spotify. Skipped.")
    return song_uris

# Example usage:
tracks = search_song(song_names)
print(tracks)


def create_playlist(name, description=""):
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user=user_id, name=name, public=True, description=description)
    print(f"Playlist '{name}' created.")
    return playlist["id"]

playlist_id = create_playlist(f"{date} Billboard 100", "A playlist of my favorite songs")


def add_tracks_to_playlist(playlist_id, track_uris):
    sp.playlist_add_items(playlist_id, track_uris)
    print(f"Added {len(track_uris)} songs to the playlist.")

add_tracks_to_playlist(playlist_id, tracks)