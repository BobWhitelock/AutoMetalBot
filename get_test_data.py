#!/usr/bin/env python3

import praw

reddit = praw.Reddit(user_agent='AutoMetalBot-0.1 /u/AutoMetalBot bob.whitelock1@gmail.com')

subreddit = reddit.get_subreddit('HeadBangToThis')

with open('HeadBangToThis', 'w') as f:
    for submission in subreddit.get_new(limit=20):
        f.write(submission.title + '|' + submission.url + '\n')