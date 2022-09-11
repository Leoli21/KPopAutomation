import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

#ID: f4861c4efd8743e2a66e63fdf1d42771
#Secret: ffe1e86ffe5641de99f085f599fee693

scope = 'playlist-modify-public'
username = 'kratoic'

token = SpotifyOAuth(scope=scope, username=username)

spotifyObject = spotipy.Spotify(auth_manager=token)

# create the playlist

playlist_name = input('Enter a  playlist name:')
playlist_description = input('Enter a playlist description:')

spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)

user_input = input('Enter the song: ')
list_of_songs = []

while user_input != 'quit':
    result = spotifyObject.search(q=user_input)
    # print(json.dumps(result, sort_keys=4, indent=4))
    list_of_songs.append(result['tracks']['items'][0]['uri'])
    user_input = input('Enter the song: ')

prePlayList = spotifyObject.user_playlists(user=username)
playlist = prePlayList['items'][0]['id']

spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=list_of_songs)



