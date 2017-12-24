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
    for submission in subreddit.hot(limit=20):
        #print(submission.title)
        for comment in submission.comments:
            if re.search("VinylDealBot",comment.body, re.IGNORECASE):

                # Get the artist name
                artist = " ".join(comment.body.split()[1:])
                print(comment.author.name + " wants alerts for " + artist)
                # Create artist obj
                created = comment.created_utc
                print (str(created))
                username = comment.author.name
                if not user_exists(c, username):
                    create_new_user(conn, c, username)
                if not user_has_artist(c, username, artist):
                    insert_artist(conn, c, username, artist, created)
                    comment.reply("**VinylDealBot!**\n\nYou will now receive messages when albums by " + artist + " go on sale!\n\nTo use me simply comment 'VinylDealBot [artist name]'")
                    os.sleep(5)

def get_template(artist, title, url):
    return '''
    VinylDealBot! on [r/VinylDeals](http://reddit.com/r/VinylDeals)
    You have been alerted that
    **''' + artist + "** is on sale today. \n" + title + "\n" + url



def send_alert(reddit, template, artist, username):
    reddit.redditor(username).message('VinylBotAlert! for ' + artist,  template)

def alert():
    users = [user[1] for user in get_users(c)]

    for submission in subreddit.hot(limit=10):
        # print(submission.title)
        url = submission.url
        for user in users:
            artists =  [artist[0] for artist in get_user_artists(c, user)]
            for artist in artists:
                if re.search(artist, submission.title, re.IGNORECASE):
                    if not alert_sent(c, user, artist, url):
                        template = get_template(artist, submission.title, url)
                        send_alert(reddit, template, artist, user)
                        create_new_alert_entry(conn, c, user, artist, url)
                        print("Sent message to " + user + "for \t" + artist + "\n" + submission.title)






while True:
    print ("Reading posts")
    readPosts()
    print ("checking alerts")
    alert()

