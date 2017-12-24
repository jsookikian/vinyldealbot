import praw
import pdb
import re
import os
import sqlite3
from db import *

conn =  sqlite3.connect('alerts.db')
c = conn.cursor()


# # reddit = praw.Reddit('VinylDealBot')
reddit = praw.Reddit(client_id='kMDo6xQ-K4bAFA',
                     client_secret='DqcJud81ZEdCfPUb4D7eEim-wFc',
                     password='4mV-6RV-tTm-zmu',
                     user_agent='VinylAlert0.1',
                     username='VinylDealBot')

print(reddit.user.me())
subreddit = reddit.subreddit("vinyldeals")

def readPosts():
    for submission in subreddit.hot(limit=10):
        #print(submission.title)
        for comment in submission.comments:
            if re.search("!VinylDealBot",comment.body, re.IGNORECASE):

                # Get the artist name
                artist = " ".join(comment.body.split()[1:])
                print(comment.author.name + " wants alerts for " + artist)
                # Create artist obj
                created = comment.created_utc
                print (str(created))
                username = comment.author.name
                if (not userExists(c, username)):
                    createUser(conn, c, username)
                insertArtist(conn, c, username, artist, created)

def alert():
    artists = getAllArtists(c)
    for submission in subreddit.hot(limit=300):
        # print(submission.title)
        for artist in artists:
            if re.search(artist, submission.title, re.IGNORECASE):

                #TODO Send out messages for 1 month on artist name


artists = getUserArtists(c, 'jsook724')
print (artists)


while True:
    readPosts()
    alert()

