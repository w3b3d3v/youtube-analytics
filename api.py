import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()

STRAPI_API_TOKEN = os.getenv("STRAPI_API_TOKEN")
API_URL= os.getenv("API_URL")
HEADERS = {
    "Authorization": f"bearer {STRAPI_API_TOKEN}"
}
POST_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"bearer {STRAPI_API_TOKEN}"
}

class Playlist:
    def get_all(self):
        req = requests.get(url=os.getenv("API_URL") + "playlists?populate=*", headers=HEADERS)
        return req.text
    
    def get_by_id(self, playlist_id):
        req = requests.get(url=os.getenv("API_URL") + f"playlists/{playlist_id}?populate=*", headers=HEADERS)
        return json.dumps(req.text)
    
    def insert(self, playlist_data):
        json_data = json.dumps(playlist_data)
        res = requests.post(os.getenv("API_URL") + "playlists/createOrUpdate", headers=POST_HEADERS, data=json_data)
        return res.text

class Video:
    def get_all(self):
        req = requests.get(url=os.getenv("API_URL") + "videos?populate=*", headers=HEADERS)
        return req.text.json()

    def get_by_id(self, video_id):
        req = requests.get(url=os.getenv("API_URL") + "videos/{video_id}?populate=*", headers=HEADERS)
        return req.text

    def insert(self, video_data):
        json_data = json.dumps(video_data)
        res = requests.post(os.getenv("API_URL") + "videos/createOrUpdate", headers=POST_HEADERS, data=json_data, params={"populate":"playlists"})
        return res.text
