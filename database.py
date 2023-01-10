
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
load_dotenv()

class Database:
    def __init__(self) -> None:
        self.db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE"),
            port=(os.getenv("DB_PORT") or 3306)
        )

    def create_cursor(self):
       return self.db.cursor()
        
    def create_playlists_table(self, cursor):
        table_sql = """CREATE TABLE IF NOT EXISTS playlists (id INT AUTO_INCREMENT PRIMARY KEY, playlist_id VARCHAR(255) UNIQUE, publishedAt DATE, playlist_name VARCHAR(255));"""
        if not cursor:
            return False
        try:
            cursor.execute(table_sql)
            return True
        except Error as e:
            print(e)
            return False
    
    def insert_playlist(self, cursor, data):
        insert_sql = """REPLACE INTO playlists (playlist_id, publishedAt, playlist_name) VALUES (%s, %s, %s);"""
        try:
            cursor.execute(insert_sql, data)
            self.db.commit()
            return True

        except Error as e:
            print(e)
            return False

    def get_inserted_playlists(self, cursor):
        try:
            cursor.execute("""SELECT * FROM playlists;""")
            response = cursor.fetchall()
            return response

        except Error as e:
            print(e)
            return False
    
    def get_playlist_id_by_id(self, cursor, playlist_id):
        try:
            cursor.execute(f"""SELECT id FROM playlists WHERE playlist_id = '{playlist_id}';""")
            response =  cursor.fetchall()
            return response

        except Error as e:
            print(e)
            return False

    def create_videos_table(self, cursor):
        table_sql = """CREATE TABLE IF NOT EXISTS videos (id INT AUTO_INCREMENT PRIMARY KEY, video_id VARCHAR(255) UNIQUE, title VARCHAR(255), publishedAt DATE, position INT);"""
        if not cursor:
            return False
        try:
            cursor.execute(table_sql)
            return True
        except Error as e:
            print(e)
            return False
    
    def insert_videos_data(self, cursor, data):
        insert_sql = """REPLACE INTO videos (video_id, title, publishedAt, position) VALUES (%s, %s, %s, %s);"""
        
        try:
            cursor.execute(insert_sql, data)
            self.db.commit()
            return cursor.lastrowid

        except Error as e:
            print(e)
            return False

    def create_video_playlists_table(self, cursor):
        table_sql = """CREATE TABLE IF NOT EXISTS videos_playlists (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            video_id INTEGER NOT NULL, 
            playlist_id  INTEGER NOT NULL,
            FOREIGN KEY(video_id) REFERENCES videos (id), 
            FOREIGN KEY(playlist_id) REFERENCES playlists(id)
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
        insert_sql = """INSERT INTO videos_playlists (video_id, playlist_id) VALUES (%s, %s);"""
        try:
            cursor.execute(insert_sql, data)
            self.db.commit()
            return cursor.lastrowid

        except Error as e:
            print(e)
            return False

    def create_analytics_table(self, cursor):
        table_sql = """CREATE TABLE IF NOT EXISTS analytics (id integer PRIMARY KEY, date VARCHAR(255), estimatedMinutesWatched INTEGER, views INTEGER, likes INTEGER, subscribersGained INTEGER, comments INTEGER, averageViewDuration INTEGER);"""
        if not cursor:
            return False
        try:
            cursor.execute(table_sql)
            self.db.commit()
            return True
        except Error as e:
            print(e)
            return False

    def insert_analytics_data(self, cursor, data):
        insert_sql = """INSERT INTO analytics (date, estimatedMinutesWatched, views, likes, subscribersGained, comments, averageViewDuration) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        
        try:
            cursor.execute(insert_sql, data)
            self.db.commit()
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