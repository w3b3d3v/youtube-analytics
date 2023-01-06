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


# Disable OAuthlib's HTTPs verification when running locally.
# *DO NOT* leave this option enabled when running in production.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

youtubeAnalytics = get_service_analytics()

request = youtubeAnalytics.reports().query(
        dimensions="video",
        endDate="2023-01-06",
        ids="channel==MINE",
        maxResults=10,
        metrics="views,likes,comments,averageViewDuration,estimatedMinutesWatched",
        sort="-views",
        startDate="2022-01-01"
    )

response = request.execute()
rows = response["rows"]

for row in rows:
    video_id = row[0]
    youtube = get_service_api()
    request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
    response = request.execute()
    row.append(response["items"][0]["snippet"]["title"])
    row.append(response["items"][0]["snippet"]["description"])
    store_response(row)

