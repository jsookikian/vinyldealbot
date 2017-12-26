import praw
import pdb
import re
import os
import time
import sqlite3
import logging
from db import *
conn = sqlite3.connect('alerts.db')
c = conn.cursor()
reddit = praw.Reddit('VinylDealBot')
subreddit = reddit.subreddit("vinyldeals")


def removeArtists(conn, cursor, comment):
    artists = " ".join(comment.body.split()[2:])
    artists = [ x.lstrip() for x in artists.split(",")]
    username = comment.author.name
    created = comment.created_utc
    for artist in artists:
        if user_has_artist(cursor, username, artist) and artist_is_active(conn, cursor, username, artist) and created > get_artist_timestamp(conn, cursor, username, artist):
            remove_artist_alert(conn, cursor, username, artist, created)
            logging.info("Removed " + artist + " from user " + username)
            reply = "**VinylDealBot**\n\nYou will no longer receive alerts for:\n\n " + artist
            comment.reply(reply)


def getCommentString(artists):
    comment = "**VinylDealBot**\n\nYou will now receive messages when the following go on sale:\n\n "
    for artist in artists:
        comment +=  artist + "\n\n"
    comment += "To get alerts, comment ```VinylDealBot [Artist | Album ] ```\n\n"
    comment += "To remove alerts, comment ```VinylDealBot Remove [Artist | Album]```\n\nSeparate multiple artists/albums with commas"
    return comment

def addArtists(conn, cursor, comment):
    # Get the artist name
    artists = " ".join(comment.body.split()[1:])
    artists = [ x.lstrip() for x in artists.split(",")]

    # Create artist obj
    created = comment.created_utc
    username = comment.author.name
    if not user_exists(cursor, username):
        create_new_user(conn, cursor, username)
    addedArtists = []
    for artist in artists:
        if not user_has_artist(cursor, username, artist):
            insert_artist(conn, cursor, username, artist, created)
            addedArtists.append(artist)
            logging.info(comment.author.name + " wants alerts for " + artist)

        if (not artist_is_active(conn, cursor, username, artist) and created > get_artist_timestamp(conn, cursor, username, artist)):
            update_artist(conn, cursor, username, artist, created)
            addedArtists.append(artist)
            logging.info(comment.author.name + " wants alerts for " + artist + " (update)")

    if (len(addedArtists) > 0):
        comment.reply(getCommentString(addedArtists))
        time.sleep(3)

def readPosts(conn, cursor):
    for submission in subreddit.hot(limit=50):
        for comment in submission.comments.list():
            cmt = comment.body.split(" ")
            if re.search("VinylDealBot",comment.body, re.IGNORECASE) and cmt[0] == "VinylDealBot":
                if re.search("Remove", comment.body, re.IGNORECASE) and cmt[1]:
                    removeArtists(conn, cursor, comment)
                else:
                    addArtists(conn, cursor, comment)


def get_template(artist, title, url, permalink):
    return '**VinylDealBot** on [r/VinylDeals](http://reddit.com/r/VinylDeals)\n\n' \
            + "[" + title + "](" + permalink + ")\n\n" \
            + url

def send_alert(reddit, template, artist, username):
    reddit.redditor(username).message('VinylDealBot: ' + artist + " on sale",  template)

def alert(conn, cursor):
    users = [user[1] for user in get_users(c)]

    for submission in subreddit.hot(limit=50):
        url = submission.url
        permalink = submission.permalink
        for user in users:
            artists =  [artist[0] for artist in get_user_artists(c, user)]
            for artist in artists:
                title = re.replace("(Lowest Price Ever", "", submission.title, count=1)
                if re.search(artist, title, re.IGNORECASE):
                    if not alert_sent(cursor, user, artist, url):
                        template = get_template(artist, submission.title, url, permalink)
                        send_alert(reddit, template, artist, user)
                        create_new_alert_entry(conn, cursor, user, artist, url)
                        logging.info("Sent message to " + user + "for " + artist + "\n" + submission.title)

if __name__ == "__main__":
    conn = sqlite3.connect('alerts.db')
    c = conn.cursor()
    logging.basicConfig(filename="vinylbot.log", level=logging.INFO, format="%(asctime)s - %(message)s")
    logging.info("Launching VinylDealBot...")

    while True:
        logging.info("Reading posts")
        readPosts(conn, c)
        logging.info("Checking alerts")
        alert(conn, c)

