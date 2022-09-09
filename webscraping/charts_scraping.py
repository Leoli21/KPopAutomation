import datetime
import requests

from googletrans import Translator
from bs4 import BeautifulSoup


'''
iChart:
    Weekly: 'http://www.instiz.net/iframe_ichart_score.htm?week=1&selyear=2015&sel={0}'.format(datetime.date.today().isocalendar()[1] - 1)

MelonChart:
    Weekly: https://www.melon.com/chart/week/index.htm

Gaon Chart:
    Weekly: https://circlechart.kr/page_chart/global.circle?termGbn=week

Billboard K-Pop 100:
    https://www.billboard.com/charts/billboard-korea-100/
'''
chart_links = {
    'iChart': 'http://www.instiz.net/iframe_ichart_score.htm?week=1&selyear=2022&sel={0}'.format(datetime.date.today().isocalendar()[1] - 1),
    'MelonChart': 'https://www.melon.com/chart/week/index.htm',
    'Gaon Chart': 'https://circlechart.kr/page_chart/global.circle?termGbn=week',
    'Billboard': 'https://www.billboard.com/charts/billboard-korea-100/'
}

# Scraper and Soup Object for iChart

# Dictionary with structure:
# Key = Song
# Value = Artist
iChartSongs = {}
iChartHTML = requests.get("https://www.instiz.net/iframe_ichart_score.htm?week=1&selyear=2015&sel=")
soup1 = BeautifulSoup(iChartHTML.text, 'lxml')
korean_translator = Translator()

# Since the first place song on chart has a unique id of 'score_1st', we can extract it's data using this
first_song = soup1.find(id='score_1st')

# Get the title and artist of the song currently in first. Luckily, both are wrapped in <b></b> tags
first_song_info = first_song.find_all('b')
song_title = first_song_info[0].text
artist = first_song_info[1].text.split(' ')[0]

# Add the first place entry into our dictionary
iChartSongs[song_title] = artist

# Get the total number of songs that are on the weekly chart
total_songs = len(soup1.find_all(class_='spage_score_item'))

# Obtain the div where the song titles are found (class='ichart_score2_song1')
song_titles = soup1.find_all(class_='ichart_score2_song1')


# Obtain the div where the rest of the song's artists lie
song_artists = soup1.find_all(class_='ichart_score2_artist1')

# Populate our dictionary with those keys and values
for i in range(total_songs):
    # Get current song's title
    curr_song = song_titles[i].text

    # Translate the current song's title to English
    translated_song = korean_translator.translate(curr_song).text

    # Get the current song's artist
    curr_artist = song_artists[i].text

    # Translate the current song's artist to English
    translated_artist = korean_translator.translate(curr_artist).text

    # Add the current translated song and translated artist as an entry to dictionary
    iChartSongs[translated_song] = translated_artist
















