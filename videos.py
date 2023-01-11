# -*- coding: utf-8 -*-
import os
from database import Database
from auth import format_env_to_secrets, youtube_authenticate
from typing import List

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
      videos.append((video["snippet"]["resourceId"]["videoId"], video["snippet"]["title"], video["snippet"]["publishedAt"].split("T")[0], video["snippet"]["position"], playlist[0]))

  created_v = db.create_videos_table(cursor=cursor)
  created_vp = db.create_video_playlists_table(cursor=cursor)
  for video in videos:
    if not created_v or not created_vp:
      return
    video_db_id = db.insert_videos_data(cursor=cursor, data=video[:-1])
    db.insert_videos_playlists(cursor=cursor, data=tuple([video_db_id, video[-1]]))

# Disable OAuthlib's HTTPs verification when running locally.
# *DO NOT* leave this option enabled when running in production.

def run():
  try:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    format_env_to_secrets()
    youtube = youtube_authenticate()
    process_playlists(youtube=youtube)
    process_videos(youtube=youtube)
    print('Done processing videos and playlists.')
    return True
  except:
    return False

# select query to query video title and playlist title on which the video is 

# SELECT videos.title, playlists.playlist_name FROM videos LEFT OUTER JOIN videos_playlists ON videos.id = videos_playlists.video_id LEFT OUTER JOIN playlists ON videos_playlists.playlist_id = playlists.id;