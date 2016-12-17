#!/usr/bin/python3
""" Script to check the latest episodes on talk python and download """

from __future__ import print_function

import re
import requests
from bs4 import BeautifulSoup

# talk python fm url. fetching the latest episode URL
URL = "https://talkpython.fm/episodes/latest/"

#Location where the podcast will be stored.
LOCATION = "/home/satish/Music/talkPython/"

#loaction_ref to check if the latest episode has already been downloaded
LOCATION_REF = LOCATION + ".talkpython"

def create_file():
    """ create the location_ref file if not present"""
    filename = open(LOCATION_REF, "w")
    filename.close()


def ref_last_download(episode):
    """ write the latest downloaded file to the location_ref"""
    last_file = open(LOCATION_REF, "w")
    last_file.write(episode)
    last_file.close()


def check_new_episode(episode):
    """check if the episode has already been downloaded or a new episode"""
    last_file = open(LOCATION_REF, "r")
    entry = last_file.readline()
    last_file.close()
    if entry == episode:
        return False
    else:
        return True

def download(episode):
    """ DOwnload episode"""
    episode_download = "https://talkpython.fm"+ episode
    print(episode_download)
    song = requests.get(episode_download)
    filename = episode.split("/")[-1]
    filename_location = LOCATION + filename
    with open(filename_location, 'wb')as episode:
        episode.write(song.content)

def fetch_episode():
    """ Fetch the latest episode from the website"""
    page = requests.get(URL).text
    page_beautifulsoup = BeautifulSoup(page, 'html.parser')
    to_download = 0
    for links in page_beautifulsoup.findAll('a'):
        if re.match("/episodes/download/", links.get('href')):
            episode = links.get('href')
            to_download = episode
    if check_new_episode(to_download):
        ref_last_download(to_download)
        download(to_download)

if __name__ == "__main__":
    #check if temp_file_exits:
    try:
        open(LOCATION_REF, 'r')
    except IOError:
        create_file()
    fetch_episode()
