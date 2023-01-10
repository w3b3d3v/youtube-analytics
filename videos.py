# -*- coding: utf-8 -*-
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from database import Database
from typing import List
from datetime import datetime
import pickle

SCOPES = ['https://www.googleapis.com/auth/youtube']

def youtube_authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "secrets.json"
    creds = None
    
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build(api_service_name, api_version, credentials=creds)

def get_playlists(youtube, channel_id: str, max_results: int = 50):
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
  db = Database()
  cursor = db.create_cursor()
  created = db.create_playlists_table(cursor=cursor)
  if not created:
      return
  return db.insert_playlist(cursor=cursor, data=tuple(row))

def process_playlists(youtube):
  playlists = get_playlists(youtube=youtube, channel_id="UCP8Qy0VXJUzE8MCJdqARrtA")
  for playlist in playlists:
    to_insert = [playlist["id"], playlist["snippet"]["publishedAt"].split("T")[0], playlist["snippet"]["title"]]
    store_playlist(row=to_insert)

def process_videos(youtube):
  db = Database()
  cursor = db.create_cursor()
  playlists = db.get_inserted_playlists(cursor=cursor)
  videos = []
  for playlist in playlists:
    videos_list = get_videos_by_playlist_id(playlist_id=playlist[1], youtube=youtube)
    for video in videos_list:
      videos.append((video["id"], video["snippet"]["title"], video["snippet"]["publishedAt"].split("T")[0], video["snippet"]["playlistId"], video["snippet"]["position"]))

  created_v = db.create_videos_table(cursor=cursor)
  for video in videos:
    if not created_v:
      return
    db.insert_videos_data(cursor=cursor, data=video)

# Disable OAuthlib's HTTPs verification when running locally.
# *DO NOT* leave this option enabled when running in production.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

youtube = youtube_authenticate()
process_playlists(youtube=youtube)
process_videos(youtube=youtube)
print('Done processing videos and playlists.')