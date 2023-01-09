import sqlite3
from sqlite3 import Error
from typing import Tuple

class Database:
    def __init__(self, db_file) -> None:
        self.db_file = db_file
    
    def __str__(self) -> str:
        return str(self.db_file)

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)
            return
        
    def create_playlists_table(self, conn):
        table_sql = """CREATE TABLE IF NOT EXISTS playlists (id integer PRIMARY KEY, playlist_id TEXT UNIQUE, publishedAt DATE, title TEXT);"""
        if not conn:
            return False
        try:
            c = conn.cursor()
            c.execute(table_sql)
            return True
        except Error as e:
            print(e)
            return False
    
    def insert_playlist(self, conn, data):
        insert_sql = """INSERT INTO playlists (playlist_id, publishedAt, playlist_name) VALUES (?, ?, ?);"""
        try:
            c = conn.cursor()
            c.execute(insert_sql, data)
            conn.commit()
            return True

        except Error as e:
            print(e)
            return False

    def get_inserted_playlists(self, conn):
        try:
            c = conn.cursor()
            response = c.execute("""SELECT * FROM playlists""").fetchall()
            return response

        except Error as e:
            print(e)
            return False
    
    def get_playlist_id_by_id(self, conn, playlist_id):
        try:
            c = conn.cursor()
            response = c.execute(f"""SELECT id FROM playlists WHERE playlist_id = '{playlist_id}'""").fetchall()
            return response

        except Error as e:
            print(e)
            return False

    def create_videos_table(self, conn):
        table_sql = """CREATE TABLE IF NOT EXISTS videos (id integer PRIMARY KEY, video_id TEXT UNIQUE, title TEXT, publishedAt DATE, playlist_id TEXT NOT NULL, FOREIGN KEY(playlist_id) REFERENCES playlists(playlist_id));"""
        if not conn:
            return False
        try:
            c = conn.cursor()
            c.execute(table_sql)
            return True
        except Error as e:
            print(e)
            return False
    
    def insert_videos_data(self, conn, data):
        insert_sql = """INSERT INTO videos (video_id, title, publishedAt, playlist_id) VALUES (?, ?, ?, ?);"""
        
        try:
            c = conn.cursor()
            c.execute(insert_sql, data)
            conn.commit()
            return c.lastrowid

        except Error as e:
            print(e)
            return False

    def create_video_playlists_table(self, conn):
        table_sql = """CREATE TABLE IF NOT EXISTS videosandplaylist (
            id INTEGER PRIMARY KEY, 
            video_db_id INTEGER NOT NULL, 
            playlist_db_id  INTEGER NOT NULL,
            FOREIGN KEY(video_db_id) REFERENCES videos (id), 
            FOREIGN KEY(playlist_db_id) REFERENCES playlists(id)
        );"""
        if not conn:
            return False
        try:
            c = conn.cursor()
            c.execute(table_sql)
            return True
        except Error as e:
            print(e)
            return False

    def insert_videos_playlists(self, conn, data):
        insert_sql = """INSERT INTO videosandplaylist (video_db_id, playlist_db_id) VALUES (?, ?);"""
        try:
            c = conn.cursor()
            c.execute(insert_sql, data)
            conn.commit()
            return c.lastrowid

        except Error as e:
            print(e)
            return False

    def create_analytics_table(self, conn):
        table_sql = """CREATE TABLE IF NOT EXISTS analytics (id integer PRIMARY KEY, date TEXT, estimatedMinutesWatched INTEGER, views INTEGER, likes INTEGER, subscribersGained INTEGER, comments INTEGER, averageViewDuration INTEGER);"""
        if not conn:
            return False
        try:
            c = conn.cursor()
            c.execute(table_sql)
            return True
        except Error as e:
            print(e)
            return False

    def insert_analytics_data(self, conn, data):
        insert_sql = """INSERT INTO analytics (date, estimatedMinutesWatched, views, likes, subscribersGained, comments, averageViewDuration) VALUES (?, ?, ?, ?, ?, ?, ?);"""
        
        try:
            c = conn.cursor()
            c.execute(insert_sql, data)
            conn.commit()
            return c.lastrowid

        except Error as e:
            print(e)
            return False
    
    def join_query(self, conn):
        query = """SELECT title, playlist_name FROM videos INNER JOIN playlists ON playlists.playlist_id = videos.playlist_id;"""
        if not conn:
            return False
        try:
            c = conn.cursor()
            res = c.execute(query).fetchall()
            return res
        except Error as e:
            print(e)
            return False