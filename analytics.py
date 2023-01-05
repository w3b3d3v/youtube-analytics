# -*- coding: utf-8 -*-

import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import utils

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

  print(response)

# Disable OAuthlib's HTTPs verification when running locally.
# *DO NOT* leave this option enabled when running in production.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

options = {
    '1': ['days', utils.day_report_time],
    '2': ['months', utils.month_report_time],
    '3': ['years', utils.year_report_time]
}
choice = input('Choose a time option for retrieving stats:\n1 - days\n2 - months\n3 - years\n')
time = input(f'How many {options[choice][0]} do you want to retrieve?\n')

youtubeAnalytics = get_service()
dates = options[choice][1](int(time))

execute_api_request (
    youtubeAnalytics.reports().query,
    ids='channel==MINE',
    startDate=dates["startDate"],
    endDate=dates["endDate"],
    metrics='estimatedMinutesWatched,views,likes,subscribersGained,comments,averageViewDuration',
    dimensions='month',
    sort='month'
)
