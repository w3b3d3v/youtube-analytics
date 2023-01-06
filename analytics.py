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

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'secrets.json'
def get_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def execute_api_request(client_library_function, **kwargs):
  response = client_library_function(
    **kwargs
  ).execute()
  return response

def store_response(response: List[List[str]]):
  rows = response["rows"]
  db = Database("analytics.sqlite")
  conn = db.create_connection()
  created = db.create_analytics_table(conn)
  if not created:
    return
  for row in rows:
    db.insert_analytics_data(conn=conn, data=tuple(row))
  print("Data stored")

# Disable OAuthlib's HTTPs verification when running locally.
# *DO NOT* leave this option enabled when running in production.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

time = input('How many months do you want to retrieve?\n')

dates = utils.month_report_time(months_ago=int(time))
youtubeAnalytics = get_service()

response = execute_api_request (
    youtubeAnalytics.reports().query,
    ids='channel==MINE',
    startDate=dates['startDate'],
    endDate= dates['endDate'],
    metrics='estimatedMinutesWatched,views,likes,subscribersGained,comments,averageViewDuration',
    dimensions='month',
    sort='month'
)

store_response(response)