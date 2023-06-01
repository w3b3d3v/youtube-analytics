# -*- coding: utf-8 -*-
import os
from auth import youtube_authenticate
import api
import json
import traceback
import logging

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
  logging.info("Getting playlists from youtube api")
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
    logging.info("Got data successfully. Preparing to insert playlists on strapi.")
    playlist_api.insert(to_insert)
    logging.info("Successfully inserted playlists on strapi.")


def process_videos(youtube):
  playlist_api = api.Playlist()
  logging.info("Getting playlists from strapi.")
  data = playlist_api.get_all()
  playlists = json.loads(data)
  
  if not playlists or not playlists["data"]:
    logging.error("Error getting playlist from strapi. Exiting...")
    return

  video_api = api.Video()

  logging.info("Getting videos from youtube api and inserting them on strapi.")
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

  logging.info("Successfully inserted videos on strapi.")

# Disable OAuthlib's HTTPs verification when running locally.
# *DO NOT* leave this option enabled when running in production.

def run():
  try:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    logging.info("Authenticating to YouTube API...")
    youtube = youtube_authenticate()
    logging.info("Successfully Authenticated to YouTube API.")

    process_playlists(youtube=youtube)
    process_videos(youtube=youtube)
    logging.info('Done processing videos and playlists.')
    return True

  except Exception:
    traceback.print_exc()
    return False

run()