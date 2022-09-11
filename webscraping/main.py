import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
from charts_scraping import *
#ID: f4861c4efd8743e2a66e63fdf1d42771
#Secret: ffe1e86ffe5641de99f085f599fee693
#Redirect URI: http://127.0.0.1:8080/

os.environ['SPOTIPY_CLIENT_ID'] = 'f4861c4efd8743e2a66e63fdf1d42771'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'ffe1e86ffe5641de99f085f599fee693'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8080/'

scope = 'playlist-modify-private, playlist-read-private'
username = 'kratoic'

token = SpotifyOAuth(scope=scope, username=username)

spotifyObject = spotipy.Spotify(auth_manager=token)




# Get current playlists of user and check to see if it contains a playlist
current_playlists = spotifyObject.current_user_playlists()

# Create a dictionary with the user's playlists
# Key = Name of Playlist
# Value = ID of Playlist
playlist_info = {}
for item in current_playlists['items']:
    playlist_info[item['name']] = item['id']


# Get the tracks of the playlist
playlist_tracks = []
# The keys store the track titles
iChart_data = get_iChart_data()
for title, artist in iChart_data.items():
    track_search_result = spotifyObject.search(q=title)
    try:
        playlist_tracks.append(track_search_result['tracks']['items'][0]['uri'])
    except:
        print(f'{title} could not be found.')
        pass

# Create the playlists if they do not already exist for current user
# Get the id of the playlist with name: 'iChart Weekly Playlist'
# If this does not exist, then create a new playlist

iChart_playlist_name = 'iChart Weekly Playlist'
iChart_playlist_ID = ''

# Playlist Already Exists, so simply replace the items in the playlist with the tracks
# Use method: playlist_replace_items(playlist_id, items)
if iChart_playlist_name in playlist_info:
    iChart_playlist_ID = playlist_info[iChart_playlist_name]
    spotifyObject.playlist_replace_items(iChart_playlist_ID, playlist_tracks)
    print('Updated iChart Music Playlist')

# Playlist does not exist, so create the new playlist with the tracks
# Use method: user_playlist_add_tracks(user, playlist_id, tracks)
else:
    iChart_playlist_description = "Auto-updating playlist of iChart's weekly ranking chart."
    spotifyObject.user_playlist_create(user=username, name=iChart_playlist_name, public=False, description=iChart_playlist_description)
    iChart_playlist_ID = spotifyObject.current_user_playlists()['items']['id']
    spotifyObject.playlist_add_items(iChart_playlist_ID, playlist_tracks)
    print('Created the new playlist and added the tracks')

