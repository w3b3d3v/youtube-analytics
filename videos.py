# -*- coding: utf-8 -*-
import os
from auth import youtube_authenticate
import api
import json
import traceback
import logging

logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO

def get_playlists(youtube, channel_id: str, max_results: int = 100):
  request = youtube.playlists().list(
    part="snippet",
    channelId=channel_id,
    maxResults=max_results
  )
  response = request.execute()
  return response["items"]

def get_videos_by_playlist_id(playlist_id: str, youtube: object, max_results: int = 50):
  logging.info(f"Getting all videos from playlist with id: {playlist_id}")

  all_videos = []
  next_page_token = None
  
  while True:
      request = youtube.playlistItems().list(
          part="snippet",
          playlistId=playlist_id,
          maxResults=min(max_results, 50),  # API limit is 50
          pageToken=next_page_token  # For pagination
      )
      response = request.execute()
      
      all_videos.extend(response["items"])
      
      next_page_token = response.get("nextPageToken")
      if next_page_token is None:
          break
  
  return all_videos

def get_all_videos(youtube: object, max_results: int = 1000):
  channel_id = get_authenticated_channel_id(youtube)
  logging.info("Getting all videos from channel with id: " + channel_id)

  all_videos = []
  next_page_token = None
  
  while True:
      request = youtube.search().list(
          part="snippet",
          type="video",
          maxResults=min(max_results, 50),  # API limit is 50
          channelId=channel_id,
          pageToken=next_page_token  # For pagination
      )
      response = request.execute()
      
      all_videos.extend(response["items"])
      if len(all_videos) >= max_results:
        break
      next_page_token = response.get("nextPageToken")
      if next_page_token is None:
        break
  
  return all_videos


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

def insert_videos_from_playlist(videos_list: list, playlist_id): 
  video_api = api.Video()
  for video in videos_list:
    to_insert = {
      "data": {
        "video_id": video["snippet"]["resourceId"]["videoId"],
        "title": video["snippet"]["title"],
        "video_published_at": video["snippet"]["publishedAt"].split("T")[0],
        "position": int(video["snippet"]["position"]),
        "playlists": [playlist_id]
      }
    }
    logging.info("Inserting video with id: " + to_insert["data"]["video_id"] + " and title: " + to_insert["data"]["title"])
    video_api.insert(to_insert)

def insert_videos(videos_list: list, playlist_id=None):
  video_api = api.Video()
  for video in videos_list:
    video_id = video["id"]["videoId"] if "id" in video else video["snippet"]["resourceId"]["videoId"]
    title = video["snippet"]["title"]
    published_at = video["snippet"]["publishedAt"].split("T")[0]
    position = int(video["snippet"]["position"]) if "position" in video["snippet"] else None

    to_insert = {
      "data": {
        "video_id": video_id,
        "title": title,
        "video_published_at": published_at,
        "position": position,
        "playlists": [playlist_id] if playlist_id else []
      }
    }

    logging.info(f"Inserting video with id: {video_id} and title: {title}")
    video_api.insert(to_insert)


def process_videos(youtube):
  playlist_api = api.Playlist()
  logging.info("Getting playlists from strapi.")
  data = playlist_api.get_all()
  playlists = json.loads(data)
  
  if not playlists or not playlists["data"]:
    logging.error("Error getting playlist from strapi. Exiting...")
    return

  logging.info("Getting videos from youtube api and inserting them on strapi.")
  for playlist in playlists["data"]:
    videos_list = get_videos_by_playlist_id(playlist_id=playlist["attributes"]["playlist_id"], youtube=youtube)  
    insert_videos_from_playlist(videos_list, playlist["id"])

  logging.info("Successfully inserted videos on strapi.")

def get_authenticated_channel_id(youtube):
    return "UCP8Qy0VXJUzE8MCJdqARrtA"


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

    # all_videos = get_all_videos(youtube)
    # logging.info("processing " + str(len(all_videos)) + " videos.")
    # insert_videos(all_videos, None)

    logging.info('Done processing videos and playlists.')
    return True

  except Exception:
    traceback.print_exc()
    return False

run()