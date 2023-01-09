
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
load_dotenv()

class Database:
    def __init__(self) -> None:
        self.db = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )

    def create_cursor(self):
       return self.db.cursor()
        
    def create_playlists_table(self, cursor):
        table_sql = """CREATE TABLE IF NOT EXISTS playlists (id INT AUTO_INCREMENT PRIMARY KEY, playlist_id TEXT UNIQUE, publishedAt DATE, title TEXT);"""
        if not cursor:
            return False
        try:
            cursor.execute(table_sql)
            return True
        except Error as e:
            print(e)
            return False
    
    def insert_playlist(self, cursor, data):
        insert_sql = """INSERT INTO playlists (playlist_id, publishedAt, playlist_name) VALUES (?, ?, ?);"""
        try:
            cursor.execute(insert_sql, data)
            cursor.commit()
            return True

        except Error as e:
            print(e)
            return False

    def get_inserted_playlists(self, cursor):
        try:
            response = cursor.execute("""SELECT * FROM playlists;""").fetchall()
            return response

        except Error as e:
            print(e)
            return False
    
    def get_playlist_id_by_id(self, conn, playlist_id):
        try:
            c = conn.cursor()
            response = c.execute(f"""SELECT id FROM playlists WHERE playlist_id = '{playlist_id}';""").fetchall()
            return response

        except Error as e:
            print(e)
            return False

    def create_videos_table(self, cursor):
        table_sql = """CREATE TABLE IF NOT EXISTS videos (id INT PRIMARY KEY, video_id TEXT UNIQUE, title TEXT, publishedAt DATE, playlist_id TEXT NOT NULL, FOREIGN KEY(playlist_id) REFERENCES playlists(playlist_id));"""
        if not cursor:
            return False
        try:
            cursor.execute(table_sql)
            return True
        except Error as e:
            print(e)
            return False
    
    def insert_videos_data(self, cursor, data):
        insert_sql = """INSERT INTO videos (video_id, title, publishedAt, playlist_id) VALUES (?, ?, ?, ?);"""
        
        try:
            cursor.execute(insert_sql, data)
            cursor.commit()
            return cursor.lastrowid

        except Error as e:
            print(e)
            return False

    def create_video_playlists_table(self, cursor):
        table_sql = """CREATE TABLE IF NOT EXISTS videosandplaylist (
            id INT PRIMARY KEY, 
            video_db_id INTEGER NOT NULL, 
            playlist_db_id  INTEGER NOT NULL,
            FOREIGN KEY(video_db_id) REFERENCES videos (id), 
            FOREIGN KEY(playlist_db_id) REFERENCES playlists(id)
        );"""
        if not cursor:
            return False
        try:
            cursor.execute(table_sql)
            return True
        except Error as e:
            print(e)
            return False

    def insert_videos_playlists(self, cursor, data):
        insert_sql = """INSERT INTO videosandplaylist (video_db_id, playlist_db_id) VALUES (?, ?);"""
        try:
            cursor.execute(insert_sql, data)
            cursor.commit()
            return cursor.lastrowid

        except Error as e:
            print(e)
            return False

    def create_analytics_table(self, cursor):
        table_sql = """CREATE TABLE IF NOT EXISTS analytics (id integer PRIMARY KEY, date TEXT, estimatedMinutesWatched INTEGER, views INTEGER, likes INTEGER, subscribersGained INTEGER, comments INTEGER, averageViewDuration INTEGER);"""
        if not cursor:
            return False
        try:
            cursor.execute(table_sql)
            return True
        except Error as e:
            print(e)
            return False

    def insert_analytics_data(self, cursor, data):
        insert_sql = """INSERT INTO analytics (date, estimatedMinutesWatched, views, likes, subscribersGained, comments, averageViewDuration) VALUES (?, ?, ?, ?, ?, ?, ?);"""
        
        try:
            cursor.execute(insert_sql, data)
            cursor.commit()
            return cursor.lastrowid

        except Error as e:
            print(e)
            return False
    
    def join_query(self, cursor):
        query = """SELECT title, playlist_name FROM videos INNER JOIN playlists ON playlists.playlist_id = videos.playlist_id;"""
        if not cursor:
            return False
        try:
            res = cursor.execute(query).fetchall()
            return res
        except Error as e:
            print(e)
            return False