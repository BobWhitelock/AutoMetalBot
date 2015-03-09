#!/usr/bin/env python3

# TODO:
# include song title when deciding between choices - search discography for match
# use genre to decide between potential choices - fuzzy match?
# determine if api has up-to-date info - if not is this ok?
# tidy up

import re
import sys
import time

import praw
import requests

SUBREDDIT = 'test'
USER_AGENT = 'AutoMetalBot-0.1 /u/AutoMetalBot bob.whitelock1@gmail.com'
METAL_ARCHIVES_API_URL = 'http://perelste.in:8001'
BAND_SEARCH_API_END_POINT = METAL_ARCHIVES_API_URL + '/api/bands/name/'
ALREADY_DONE_FILE = 'done'

class Title:

    SEPARATOR = '-'
    NON_BRACKETED_REGEX = '[^\[\]\(\)]+'
    CIRCLE_BRACKETS_REGEX = '\(([^\(\)]*)\)'
    SQUARE_BRACKETS_REGEX = '\[([^\[\]]*)\]'

    def __init__(self, title_text):
        """ Process text of a title to try and determine major features.

            Titles usually tend to conform to following structure:
            band_name <always> - song_name <always> [genre <often>] (label <often>) further_description <sometimes>
            The band name and song name almost always appear and in this
            format but other parts sometimes don't appear or are in different
            orders.
        """
        # split title along separator
        title_parts = title_text.split(Title.SEPARATOR, 1)
        if len(title_parts) == 2:
            # parse out parts of title in turn as much as possible
            self.band = title_parts[0].strip()
            self._title_remainder = title_parts[1].strip()

            self._parse_song_name()
            self._parse_genre()
            self._parse_label()

            self.further_description = self._title_remainder
        else:
            # if title not split along separator then does not conform to
            # format so can't parse, so set all fields to None
            self.band = None
            self.song = None
            self.genre = None
            self.label = None
            self.further_description = None

    def _parse_song_name(self):
        """ Parse song as everything in title remainder up to first brackets, if this exists. """
        song_name_match = re.match(Title.NON_BRACKETED_REGEX, self._title_remainder)
        if song_name_match:
            self.song = song_name_match.group().strip()
            # set remainder to be everything after match
            self._title_remainder = self._title_remainder[song_name_match.end():]
        else:
            self.song = None

    def _parse_genre(self):
        """ Parse genre as contents of first square brackets, if any exist. """
        genre_match = re.search(Title.SQUARE_BRACKETS_REGEX, self._title_remainder)
        if genre_match:
            self.genre = genre_match.group(1).strip()
            # set remainder to be everything after match
            self._title_remainder = self._title_remainder[genre_match.end():]
        else:
            self.genre = None

    def _parse_label(self):
        """ Parse label as contents of first circle brackets, if any exist. """
        label_match = re.search(Title.CIRCLE_BRACKETS_REGEX, self._title_remainder)
        if label_match:
            self.label = label_match.group(1).strip()
            # set remainder to be existing remainder with match cut
            # - sometimes info before and after circle brackets so include any of this
            self._title_remainder = (self._title_remainder[:label_match.start()] + self._title_remainder[label_match.end():]).strip()
        else:
            self.label = None


def identify(title):
    parsed_title = Title(title)
    if parsed_title.band is None:
        return None
    band_search_url = BAND_SEARCH_API_END_POINT + parsed_title.band
    band_search_response = requests.get(band_search_url)
    band_search_json = band_search_response.json()

    candidates = [band for band in band_search_json if band['name'].lower() == parsed_title.band.lower()]

    number_candidates = len(candidates)
    if number_candidates == 0:
        return None
    elif number_candidates == 1:
        return candidates[0]['url']
    else:
        print('\nPossibles: ' + str(candidates) + '\n')
        return None


class AlreadyDone:
    def __init__(self):
        self.done = self._read()

    def _read(self):
        try:
            with open(ALREADY_DONE_FILE) as f:
                return {line.strip() for line in f.readlines()}
        except FileNotFoundError:
            return set()

    def add(self, submission_id):
        try:
            with open(ALREADY_DONE_FILE, 'a') as f:
                f.write(submission_id + '\n')
                self.done.add(submission_id)
        except Exception as e:
            # TODO log this
            print('Caught exception: ', e)
            sys.exit(1)

    def __contains__(self, submission_id):
        return submission_id in self.done


def run():
    already_done = AlreadyDone()
    reddit = praw.Reddit(user_agent=USER_AGENT)
    reddit.login()
    while True:
        subreddit = reddit.get_subreddit(SUBREDDIT)
        for submission in subreddit.get_new(limit=10):
            if submission.id not in already_done:
                band_page = identify(submission.title)
                if band_page is not None:
                    # submission.add_comment(band_page)
                    print('would have written: ' + band_page)
                already_done.add(submission.id)


        time.sleep(30)


if __name__ == '__main__':
    run()


    # identify('Voices')

    # t = Title('Cloud Rat - Blind River [Metallic Hardcore] (Halo of Flies)')
    # print(t.band)
    # print(t.song)
    # print(t.genre)
    # print(t.label)
    # print(t.further_description)
