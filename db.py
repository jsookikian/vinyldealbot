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
            created TIMESTAMP NOT NULL,
             )
    ''')

    cursor.execute('''
        CREATE TABLE UserXArtist (
            user_id INT(11),
            artist_id INT(11),
            CONSTRAINT FKUserXArtist_userId FOREIGN KEY (user_id) REFERENCES User(id),
            CONSTRAINT FKUserXArtist_artistId FOREIGN KEY (artist_id) REFERENCES Artist(id)

            )
    ''')

    cursor.execute('''
        CREATE TABLE Alert (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username INT(11) NOT NULL,
            artist INT(11) NOT NULL,
            url varchar(400) NOT NULL)''')

def create_test_data(conn, cursor):
    users = ["jsook724"]
    create_new_user(conn, "jsook724")

    for i in range(3):
        create_new_user(cursor, "user" + str(i))
        users.append("user"+ str(i))

    for user in users:
        for i in range(10):
            ts = datetime.datetime.now().timestamp()
            insert_artist(conn, cursor, user, "Artist" + str(i), ts)

    for user in users:
        artists = get_user_artists(cursor, user)
        print ("User: " + user + "\nArtists:\n")
        for artist in artists:
            print(artist[0] + "\tts: " + str(artist[1]))

def test_remove(conn, cursor):
    users = ["jsook724"]
    # create_new_user(conn, "jsook724")
    artists = ["Steppenwolf"]
    print ("adding steppenwolf")
    ts = datetime.datetime.now().timestamp()
    insert_artist(conn, cursor, users[0], "Steppenwolf", ts)

    artists = get_user_artists(cursor, users[0])
    print("User: " + users[0] + "\nArtists:\n")
    for artist in artists:
        print(artist[0] + "\tts: " + str(artist[1]))

    remove_artist_alert(conn, cursor, "jsook724", "Steppenwolf", datetime.datetime.timestamp())
    print ("Removing steppenwolf")
    artists = get_user_artists(cursor, users[0])
    print("User: " + users[0] + "\nArtists:\n")
    for artist in artists:
        print(artist[0] + "\tts: " + str(artist[1]))


def remove_artist_alert(conn, cursor, username, artist, created):
    if user_exists(cursor, username) and user_has_artist(cursor, username, artist):
        userid = get_user_id(cursor, username)
        artistid =get_artist_id(cursor, username, artist)
        results = cursor.execute("Update ARTIST SET Active=0, created= ? WHERE id=?", (created, artistid,))
        conn.commit()

def update_artist(conn, cursor, username, artist, created):
    if user_exists(cursor, username) and user_has_artist(cursor, username, artist):
        userid = get_user_id(cursor, username)
        artistid = get_artist_id(cursor, username, artist)
        results = cursor.execute("Update ARTIST SET Active=1, created= ? WHERE id=?", (created, artistid,))
        conn.commit()

def create_new_user(conn, cursor, username):
    if not user_exists(cursor, username):
        results = cursor.execute("INSERT INTO User(name) VALUES(?)", (username,))
        conn.commit()
        return results.lastrowid
    else:
        return -1

def user_exists(cursor, username):
    results = cursor.execute("SELECT name FROM User WHERE name=?", (username,))
    row = results.fetchone()
    if row is None:
        return False
    else:
        return True

def get_user_id(cursor, username):
    results = cursor.execute("SELECT id FROM User WHERE name=?", (username,))
    row = results.fetchone()
    return row[0]


def get_artist_id(cursor, username, artist):
    if user_has_artist(cursor, username, artist):
        userid = get_user_id(cursor, username)
        results = cursor.execute('''
            SELECT Artist.id FROM User
                JOIN  UserXArtist ON User.id = user_id
                JOIN Artist ON Artist.id = artist_id
                WHERE Artist.name = ?
                AND User.name = ?''' ,(artist, username))
        rows = cursor.fetchone()
        artistid = rows[0]
        return artistid


def insert_artist(conn, cursor, username, artist, created):
    if (not user_exists(cursor, username)):
        return -1
    userid = get_user_id(cursor, username)
    results = cursor.execute("INSERT INTO Artist(name, created, active) VALUES(?, ?, ?)", (artist, created, 1))
    artistid = cursor.lastrowid
    results = cursor.execute("INSERT INTO UserXArtist(user_id, artist_id) VALUES(?, ?)", (userid, artistid))
    conn.commit()

def artist_is_active(conn, cursor, username, artist):
    if user_exists(cursor, username):
        userid = get_user_id(cursor, username)
        artistid = get_artist_id(cursor, username, artist)
        results = cursor.execute('''
            SELECT active FROM Artist
                JOIN  UserXArtist ON artist_id = Artist.id
                JOIN User ON user_id = User.id
                WHERE User.name = ?
                AND Artist.name = ?
                ''', (username, artist)
        )
        row = results.fetchone()
        if row[0] == 1:
            return True
        else:
            return False


def get_artist_timestamp(conn, cursor, username, artist):
    if user_exists(cursor, username):
        userid = get_user_id(cursor, username)
        artistid = get_artist_id(cursor, username, artist)
        results = cursor.execute('''
            SELECT created FROM Artist
                JOIN  UserXArtist ON artist_id = Artist.id
                JOIN User ON user_id = User.id
                WHERE User.name = ?
                AND Artist.name = ?
                ''', (username, artist)
        )
        row = results.fetchone()
        return row[0]


def get_user_artists(cursor, username):
    if (not user_exists(cursor, username)):
        return -1
    userid = get_user_id(cursor, username)
    results = cursor.execute('''
        SELECT Artist.name, Artist.created FROM Artist
            JOIN  UserXArtist ON artist_id = Artist.id
            JOIN User ON user_id = User.id
            WHERE User.name = ? AND Artist.active=1''' ,(username,) )

    rows = cursor.fetchall()
    return rows

def get_users(cursor):
    results = cursor.execute('SELECT * FROM USER')
    return results.fetchall()

def user_has_artist(cursor, username, artist):
    results = cursor.execute('''
        SELECT count(*) FROM Artist
            JOIN  UserXArtist ON artist_id = Artist.id
            JOIN User ON user_id = User.id
            WHERE User.name = ?
            AND Artist.name = ?
            ''', (username,artist)
    )


    row = results.fetchone()
    if row[0] >= 1:
        return True
    else:
        return False

def alert_sent(cursor, username, artist, url):
    results = cursor.execute('''
      SELECT count(*) FROM Alert
      WHERE username=?
      AND artist=?
      AND url=?
      ''', (username,artist, url))
    row = results.fetchone()
    if row[0] == 0:
        return False
    else:
        return True

def create_new_alert_entry(conn, cursor, username, artist, url):
    results = cursor.execute("INSERT INTO Alert(username, artist, url) VALUES(?, ?, ?)", (username,artist, url))
    conn.commit()
# init_tables(c)
# create_test_data(conn, c)
# test_remove(conn, c)

def update_tables(conn, cursor):
    # cursor.execute('''
    #     ALTER TABLE Artist
    #     ADD COLUMN active INTEGER
    # ''')

    cursor.execute('''
        UPDATE Artist
        SET active = 1
        WHERE name <> ''

    ''')
    conn.commit()


# update_tables(conn, c)
