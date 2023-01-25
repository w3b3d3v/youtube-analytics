import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()

def youtube_authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    return build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
