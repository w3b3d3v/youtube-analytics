# -*- coding: utf-8 -*-
import os
from auth import youtube_authenticate
import api
import json
import traceback

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


def process_playlists(youtube):
  playlists = get_playlists(youtube=youtube, channel_id="UCP8Qy0VXJUzE8MCJdqARrtA")
  playlist_api = api.Playlist()

  for playlist in playlists:
    to_insert = {
      "data": {
        "playlist_id": playlist["id"],
        "playlist_name": playlist["snippet"]["title"],
        "playlist_published_at": playlist["snippet"]["publishedAt"].split("T")[0]
      }
    }
    playlist_api.insert(to_insert)


def process_videos(youtube):
  playlist_api = api.Playlist()
  data = playlist_api.get_all()
  playlists = json.loads(data)
  
  if not playlists:
    return

  video_api = api.Video()

  for playlist in playlists["data"]:
    videos_list = get_videos_by_playlist_id(playlist_id=playlist["attributes"]["playlist_id"], youtube=youtube)


    for video in videos_list:
      to_insert = {
        "data": {
          "video_id": video["snippet"]["resourceId"]["videoId"],
          "title": video["snippet"]["title"],
          "video_published_at": video["snippet"]["publishedAt"].split("T")[0],
          "position": int(video["snippet"]["position"]),
          "playlists": [playlist["id"]]
        }
      }
      video_api.insert(to_insert)

# Disable OAuthlib's HTTPs verification when running locally.
# *DO NOT* leave this option enabled when running in production.

def run():
  try:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    youtube = youtube_authenticate()
    process_playlists(youtube=youtube)
    process_videos(youtube=youtube)
    print('Done processing videos and playlists.')
    return True

  except Exception:
    traceback.print_exc()
    return False

run()