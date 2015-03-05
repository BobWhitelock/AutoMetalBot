#!/usr/bin/env python3

# TODO:
# include song title when deciding between choices - search discography for match
# use genre to decide between potential choices - fuzzy match?
# determine if api has up-to-date info - if not is this ok?
# tidy up

import time

import praw
import requests

METAL_ARCHIVES_API_URL = 'http://perelste.in:8001'
BAND_SEARCH_API_END_POINT = METAL_ARCHIVES_API_URL + '/api/bands/name/'

# reddit = praw.Reddit(user_agent='AutoMetalBot-0.1 /u/AutoMetalBot bob.whitelock1@gmail.com')

# reddit.login()

# while True:
# subreddit = reddit.get_subreddit('HeadBangToThis')
# for submission in subreddit.get_new(limit=50):
#     print(submission.title + )

    # time.sleep(60)

def identify(title):
    band_name_in_title = title.split('-')[0].strip()
    band_search_url = BAND_SEARCH_API_END_POINT + band_name_in_title + '/'
    band_search_response = requests.get(band_search_url)
    potential_bands = band_search_response.json()

    bands_with_exact_name = []
    for potential_band in potential_bands:
        if potential_band['name'].lower() == band_name_in_title.lower():
            bands_with_exact_name.append(potential_band)

    number_exact_matches = len(bands_with_exact_name)
    if number_exact_matches == 0:
        return ''
    elif number_exact_matches == 1:
        return bands_with_exact_name[0]['url']
    else:
        print('\nPossibles: ' + str(bands_with_exact_name) + '\n')
        return ''

    time.sleep(1)


if __name__ == '__main__':
    identify('Voices')