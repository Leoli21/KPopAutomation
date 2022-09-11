import datetime
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def get_iChart_data():
    # Dictionary with structure:
    # Key = Song
    # Value = Artist
    iChartSongs = {}

    # Scraper and Soup Object for iChart Music Chart
    iChartHTML = requests.get(chart_links['iChart'])
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
        #translated_song = korean_translator.translate(curr_song).text

        # Get the current song's artist
        curr_artist = song_artists[i].text

        # Translate the current song's artist to English
        #translated_artist = korean_translator.translate(curr_artist).text

        # Add the current translated song and translated artist as an entry to dictionary
        #iChartSongs[translated_song] = translated_artist
        iChartSongs[curr_song] = curr_artist
    return iChartSongs

def get_MelonChart_data():
    # Dictionary with structure:
    # Key = Song
    # Value = Artist
    melonChartSongs = {}

    # Scraper and Soup Object for Melon Chart
    melonChartHTML = requests.get(chart_links['MelonChart'], headers={"User-Agent": "XY"})

    soup2 = BeautifulSoup(melonChartHTML.text, 'lxml')
    korean_translator = Translator()

    # Get total songs in chart
    total_songs = len(soup2.find_all(class_='ellipsis rank01'))

    # Get the first 50 song titles
    song_titles = soup2.find_all(class_='rank01')

    song_artists = soup2.find_all(class_='checkEllipsis')

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
        melonChartSongs[translated_song] = translated_artist
        #melonChartSongs[curr_song] = curr_artist
    return melonChartSongs

def get_GaonChart_data():
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    # Dictionary with structure:
    # Key = Song
    # Value = Artist
    gaonChartSongs = {}

    korean_translator = Translator()
    # Scraper and Selenium Object for Melon Chart
    gaonChartHTML = chart_links['Gaon Chart']
    driver.get(gaonChartHTML)

    # Need to access the .text attribute and .strip() to get the titles formatted
    song_titles = []

    # Need to access the .text attribute and .strip() to get the artists formatted
    song_artists = []
    try:
        song_titles = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.font-bold.mb-2'))
        )
        song_artists = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.text-sm.text-gray-400.font-bold'))
        )
    except:
        driver.quit()

    for i in range(100):
        # Get current song's title
        curr_song = song_titles[i].text.strip()

        # Translate the current song's title to English
        translated_song = korean_translator.translate(curr_song).text

        # Get the current song's artist
        curr_artist = song_artists[i].text.strip()

        # Translate the current song's artist to English
        translated_artist = korean_translator.translate(curr_artist).text

        # Add the current translated song and translated artist as an entry to dictionary
        gaonChartSongs[translated_song] = translated_artist
        #gaonChartSongs[curr_song] = curr_artist

    driver.quit()
    return gaonChartSongs

def get_BillboardChart_data():
    # Dictionary with structure:
    # Key = Song
    # Value = Artist
    billboardChartSongs = {}

    # Scraper and Soup Object for Melon Chart
    billboardHTML = requests.get(chart_links['Billboard'])

    soup2 = BeautifulSoup(billboardHTML.text, 'lxml')

    # Get total songs in chart
    total_songs = len(soup2.find_all(class_='o-chart-results-list-row-container'))

    # Get the song's from the chart
    song_titles = soup2.find_all('h3', class_='a-font-primary-bold-s')
    song_titles = song_titles[2:]

    # Get the artists from the chart
    song_artists = soup2.find_all('span', class_='a-no-trucate')

    # Populate our dictionary with those keys (song) and values (artist)
    for i in range(total_songs):
        # Get current song's title
        curr_song = song_titles[i].text.strip()

        # Get the current song's artist
        curr_artist = song_artists[i].text.strip()

        # Add the current translated song and translated artist as an entry to dictionary
        billboardChartSongs[curr_song] = curr_artist

    return billboardChartSongs

if __name__ == '__main__':
    #iChartSongs = get_iChart_data()
    #melonChartSongs = get_MelonChart_data()
    #gaonChartSongs = get_GaonChart_data()
    #billboardChartSongs = get_BillboardChart_data()
    pass






























