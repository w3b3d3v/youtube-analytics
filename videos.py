# -*- coding: utf-8 -*-

import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import utils
from database import Database
from typing import List

SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRETS_FILE = 'secrets.json'

def get_service_api():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def get_service_analytics():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build('youtubeAnalytics', 'v2', credentials = credentials)

def execute_api_request(client_library_function, **kwargs):
  response = client_library_function(
    **kwargs
  ).execute()
  return response

def store_response(row: List):
    db = Database("analytics.sqlite")
    conn = db.create_connection()
    created = db.create_videos_table(conn=conn)
    if not created:
        return
    return db.insert_videos_data(conn=conn, data=tuple(row))

def get_playlists(channel_id: str, max_results: int = 50):
  youtube = get_service_api()
  request = youtube.playlists().list(
    part="snippet",
    channelId=channel_id,
    maxResults=max_results
  )
  response = request.execute()
  return response["items"]

def get_videos_by_playlist_id(playlist_id: str, youtube: object, max_results: int = 50):
  request = youtube.playlistItems().list(
    part="snippet",
    playlistId=playlist_id,
    maxResults=max_results
  )
  response = request.execute()
  return response["items"]

def store_playlist(row: List):
  db = Database("analytics.sqlite")
  conn = db.create_connection()
  created = db.create_playlists_table(conn=conn)
  if not created:
      return
  return db.insert_playlist(conn=conn, data=tuple(row))

def process_playlists():
  playlists = get_playlists(channel_id="UCP8Qy0VXJUzE8MCJdqARrtA")
  for playlist in playlists:
    to_insert = []
    to_insert.append(playlist["id"])
    to_insert.append(playlist["snippet"]["publishedAt"])
    to_insert.append(playlist["snippet"]["title"])

    store_playlist(row=to_insert)

def process_videos():
  db = Database("analytics.sqlite")
  conn = db.create_connection()
  playlists = db.get_inserted_playlists(conn)
  videos = []
  youtube = get_service_api()
  for playlist in playlists:
    videos_list = get_videos_by_playlist_id(playlist_id=playlist[1], youtube=youtube)
    for video in videos_list:
      videos.append((video["id"], video["snippet"]["title"], video["snippet"]["publishedAt"], video["snippet"]["playlistId"]))

  created_v = db.create_videos_table(conn)
  for video in videos:
    if not created_v:
      return
    video_id = db.insert_videos_data(conn, video)

# Disable OAuthlib's HTTPs verification when running locally.
# *DO NOT* leave this option enabled when running in production.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


# process_playlists()
# process_videos()

db = Database("analytics.sqlite")
conn = db.create_connection()
print(db.join_query(conn))

  
# get list of playlists by youtube.playlists.list() and store it in a playlists database

# then get playlistItems by playlist and store them

# many to many relationship ->
# video: PK video id, other video fields
# playlist: PK playlist id, other fields
# video_playlist: PF video id, PF playlist id