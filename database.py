import sqlite3
from sqlite3 import Error

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

    def create_videos_table(self, conn):
        table_sql = """CREATE TABLE IF NOT EXISTS videos (id integer PRIMARY KEY, video_id TEXT, views INTEGER, likes INTEGER, comments INTEGER, averageViewDuration INTEGER, estimatedMinutesWatched INTEGER, title TEXT, description TEXT);"""
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
        insert_sql = """INSERT INTO videos (video_id, views, likes, comments, averageViewDuration, estimatedMinutesWatched, title, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
        
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