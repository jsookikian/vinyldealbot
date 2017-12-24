import sqlite3
import datetime
conn =  sqlite3.connect('alerts.db')
c = conn.cursor()


def init_tables(cursor):
    cursor.execute('''
        CREATE TABLE User (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         name varchar(250) NOT NULL
        )
      ''')

    cursor.execute('''
        CREATE TABLE Artist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name varchar(250) NOT NULL,
            created TIMESTAMP NOT NULL )
    ''')

    cursor.execute('''
        CREATE TABLE UserXArtist (
            user_id INT(11),
            artist_id INT(11),
            CONSTRAINT FKUserXArtist_userId FOREIGN KEY (user_id) REFERENCES User(id),
            CONSTRAINT FKUserXArtist_artistId FOREIGN KEY (artist_id) REFERENCES Artist(id) )
    ''')

def create_test_data(conn, cursor):
    users = ["jsook724"]
    create_new_user(conn, "jsook724")

    for i in range(3):
        create_new_user("user" + str(i))
        users.append("user "+ str(i))

    for user in users:
        for i in range(10):
            ts = datetime.datetime.now().timestamp()
            insert_artist(conn, cursor, user, "Artist" + str(i), ts)

    for user in users:
        artists = get_user_artists(cursor, user)
        print ("User: " + user + "\nArtists:\n")
        for artist in artists:
            print(artist[0] + "\tts: " + artist[1])





def create_new_user(cursor, username):
    if not user_exists(cursor, username):

        results = cursor.execute("INSERT INTO User(name) VALUES(?)", (username))
        conn.commit()
        return cursor.lastrowid
    else:
        return -1

def user_exists(cursor, username):
    results = cursor.execute("SELECT name FROM User WHERE name=?", (username))
    row = cursor.fetchone()
    if row is None:
        return False
    else:
        return True

def get_user_id(cursor, username):
    results = cursor.execute("SELECT id FROM User WHERE name=?", (username))
    row = cursor.fetchone()
    return row

def insert_artist(conn, cursor, username, artist, created):
    if (not user_exists(cursor, username)):
        return -1
    userid = get_user_id(cursor, username)
    results = cursor.execute("INSERT INTO Artist(name, created) VALUES(?, ?)", (artist, created))
    artistid = cursor.lastrowid
    results = cursor.execute("INSERT INTO UserXArtist(user_id, artist_id) VALUES(?, ?)", (userid, artistid))
    conn.commit()

def get_user_artists(cursor, username):
    if (not user_exists(cursor, username)):
        return -1
    userid = get_user_id(cursor, username)
    results = cursor.execute('''
        SELECT Artist.name, Artist.created FROM Artist
            JOIN  UserXArtist ON artist_id = Artist.id
            JOIN User ON user_id = User.id
            WHERE User.name = ?''' ,(username) )

    rows = cursor.fetchall()
    return rows

init_tables(c)
create_test_data(conn, c)
