import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
from charts_scraping import *
from datetime import date

import base64

# ID: f4861c4efd8743e2a66e63fdf1d42771
# Secret: ffe1e86ffe5641de99f085f599fee693
# Redirect URI: http://127.0.0.1:8080/

os.environ['SPOTIPY_CLIENT_ID'] = 'f4861c4efd8743e2a66e63fdf1d42771'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'ffe1e86ffe5641de99f085f599fee693'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8080/'

scope = 'playlist-modify-private, playlist-read-private'
username = 'kratoic'

token = SpotifyOAuth(scope=scope, username=username)

spotifyObject = spotipy.Spotify(auth_manager=token)


def get_user_playlist_info():
    # Get current playlists of user and check to see if it contains a playlist
    current_playlists = spotifyObject.current_user_playlists()

    # Create a dictionary with the user's playlists
    # Key = Name of Playlist
    # Value = ID of Playlist
    playlist_info = {}
    for item in current_playlists['items']:
        playlist_info[item['name']] = item['id']

    return playlist_info


def iChart_automate():
    # Stores the tracks of the playlists
    playlist_tracks = []

    # The keys store the track titles
    iChart_data = get_iChart_data()

    # Add the titles extracted from iChart to our list storing the tracks
    for title, artist in iChart_data.items():
        track_search_result = spotifyObject.search(q="track:" + title, type="track")
        try:
            playlist_tracks.append(track_search_result['tracks']['items'][0]['uri'])
        except:
            print(f'{title} by {artist}: not found.')
            pass
    # Create the playlists if they do not already exist for current user
    # Get the id of the playlist with name: 'iChart Weekly Playlist'
    # If this does not exist, then create a new playlist
    playlist_info = get_user_playlist_info()
    iChart_playlist_name = 'iChart Weekly Playlist'
    ichart_playlist_description = "Auto-updating playlist of iChart's weekly ranking chart. Last Updated: {date}".format(
        date=date.today())

    #with open(os.path.abspath('../imgs/BillboardChart.jpeg')) as playlist_img:
    #    encoded_playlist_cover_string = base64.b64encode(playlist_img.read())

    # Playlist Already Exists, so simply replace the items in the playlist with the tracks
    # Use method: playlist_replace_items(playlist_id, items)
    if iChart_playlist_name in playlist_info:
        iChart_playlist_ID = playlist_info[iChart_playlist_name]
        spotifyObject.playlist_replace_items(iChart_playlist_ID, playlist_tracks)
        spotifyObject.playlist_change_details(iChart_playlist_ID, description=ichart_playlist_description)
        print('Updated iChart Music Playlist')

    # Playlist does not exist, so create the new playlist with the tracks
    # Use method: user_playlist_add_tracks(user, playlist_id, tracks)
    else:
        spotifyObject.user_playlist_create(user=username, name=iChart_playlist_name, public=False,
                                           description=ichart_playlist_description)
        iChart_playlist_ID = get_user_playlist_info()[iChart_playlist_name]
        spotifyObject.playlist_add_items(iChart_playlist_ID, playlist_tracks)
        # Set the playist cover
        #spotifyObject.playlist_upload_cover_image(iChart_playlist_ID, encoded_playlist_cover_string)
        print('Created the new playlist and added the tracks')

def melon_automate():
    # Store the tracks that will be added to our playlist
    playlist_tracks = []

    # The keys store the track titles
    melon_data = get_MelonChart_data()

    # Add the tracks extracted from MelonChart to our list
    for title, artist in melon_data.items():
        # 86 tracks with no Korean

        track_search_result = spotifyObject.search(q="track:" + title, type="track")
        try:
            playlist_tracks.append(track_search_result['tracks']['items'][0]['uri'])
        except:
            print(f'{title} could not be found.')
            pass

    # Create the playlists if they do not already exist for current user
    # Get the id of the playlist with name: 'iChart Weekly Playlist'
    # If this does not exist, then create a new playlist
    playlist_info = get_user_playlist_info()
    melon_chart_playlist_name = 'Melon Chart Weekly Playlist'
    melon_playlist_description = "Auto-updating playlist of Melon Chart's weekly ranking chart. Last Updated: {date}".format(
        date=date.today())

    # Playlist Already Exists, so simply replace the items in the playlist with the tracks
    # Use method: playlist_replace_items(playlist_id, items)
    if melon_chart_playlist_name in playlist_info:
        melon_playlist_ID = playlist_info[melon_chart_playlist_name]
        spotifyObject.playlist_replace_items(melon_playlist_ID, playlist_tracks)
        spotifyObject.playlist_change_details(melon_playlist_ID, description=melon_playlist_description)
        print('Updated Melon Chart Music Playlist')

    # Playlist does not exist, so create the new playlist with the tracks
    # Use method: user_playlist_add_tracks(user, playlist_id, tracks)
    else:
        spotifyObject.user_playlist_create(user=username, name=melon_chart_playlist_name, public=False,
                                           description=melon_playlist_description)
        melon_playlist_ID = get_user_playlist_info()[melon_chart_playlist_name]
        spotifyObject.playlist_add_items(melon_playlist_ID, playlist_tracks)
        print('Created the new playlist and added the tracks')


def gaon_automate():
    # Store the tracks that will be added to our playlist
    playlist_tracks = []

    # The keys store the track titles
    gaon_data = get_GaonChart_data()

    # Add the tracks extracted from MelonChart to our list
    for title, artist in gaon_data.items():
        track_search_result = spotifyObject.search(q="track:" + title, type="track")
        try:
            playlist_tracks.append(track_search_result['tracks']['items'][0]['uri'])
        except:
            print(f'{title} could not be found.')
            pass

    # Create the playlists if they do not already exist for current user
    # Get the id of the playlist with name: 'iChart Weekly Playlist'
    # If this does not exist, then create a new playlist
    playlist_info = get_user_playlist_info()
    gaon_chart_playlist_name = 'Gaon Chart Weekly Playlist'
    gaon_playlist_description = "Auto-updating playlist of Gaon Chart's weekly ranking chart. Last Updated: {date}".format(
        date=date.today())

    # Playlist Already Exists, so simply replace the items in the playlist with the tracks
    # Use method: playlist_replace_items(playlist_id, items)
    if gaon_chart_playlist_name in playlist_info:
        gaon_playlist_ID = playlist_info[gaon_chart_playlist_name]
        spotifyObject.playlist_replace_items(gaon_playlist_ID, playlist_tracks)
        spotifyObject.playlist_change_details(gaon_playlist_ID, description=gaon_playlist_description)
        print('Updated Gaon Chart Music Playlist')

    # Playlist does not exist, so create the new playlist with the tracks
    # Use method: user_playlist_add_tracks(user, playlist_id, tracks)
    else:
        spotifyObject.user_playlist_create(user=username, name=gaon_chart_playlist_name, public=False,
                                           description=gaon_playlist_description)
        gaon_playlist_ID = get_user_playlist_info()[gaon_chart_playlist_name]
        spotifyObject.playlist_add_items(gaon_playlist_ID, playlist_tracks)
        print('Created the new playlist and added the tracks')


def billboard_automate():
    # Store the tracks that will be added to our playlist
    playlist_tracks = []

    # The keys store the track titles
    billboard_data = get_BillboardChart_data()

    # Add the tracks extracted from MelonChart to our list
    for title, artist in billboard_data.items():
        track_search_result = spotifyObject.search(q="track:" + title, type="track")
        try:
            playlist_tracks.append(track_search_result['tracks']['items'][0]['uri'])
        except:
            print(f'{title} could not be found.')
            pass

    # Create the playlists if they do not already exist for current user
    # Get the id of the playlist with name: 'iChart Weekly Playlist'
    # If this does not exist, then create a new playlist
    playlist_info = get_user_playlist_info()
    billboard_chart_playlist_name = 'Billboard K-Pop Chart Weekly Playlist'
    billboard_playlist_description = "Auto-updating playlist of Billboard Chart's weekly ranking chart. Last Updated: " \
                                     "{date}".format(date=date.today())

    # Playlist Already Exists, so simply replace the items in the playlist with the tracks
    # Use method: playlist_replace_items(playlist_id, items)
    if billboard_chart_playlist_name in playlist_info:
        billboard_playlist_ID = playlist_info[billboard_chart_playlist_name]
        spotifyObject.playlist_replace_items(billboard_playlist_ID, playlist_tracks)
        spotifyObject.playlist_change_details(billboard_playlist_ID, description=billboard_playlist_description)
        print('Updated Billboard Chart Music Playlist')

    # Playlist does not exist, so create the new playlist with the tracks
    # Use method: user_playlist_add_tracks(user, playlist_id, tracks)
    else:
        spotifyObject.user_playlist_create(user=username, name=billboard_chart_playlist_name, public=False,
                                           description=billboard_playlist_description)
        billboard_playlist_ID = get_user_playlist_info()[billboard_chart_playlist_name]
        spotifyObject.playlist_add_items(billboard_playlist_ID, playlist_tracks)
        print('Created the new playlist and added the tracks')

if __name__ == '__main__':
    iChart_automate()
    melon_automate()
    gaon_automate()
    billboard_automate()
