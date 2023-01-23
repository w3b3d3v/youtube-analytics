import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
HEADERS = {
    "Authorization": f"bearer {API_TOKEN}"
}
POST_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"bearer {API_TOKEN}"
}

class Playlist:
    def get_all(self):
        req = requests.get(url="http://localhost:1337/api/playlists?populate=*", headers=HEADERS)
        return req.text
    
    def get_by_id(self, playlist_id):
        req = requests.get(url=f"http://localhost:1337/api/playlist/{playlist_id}?populate=*", headers=HEADERS)
        return json.dumps(req.text)
    
    def insert(self, playlist_data):
        json_data = json.dumps(playlist_data)
       
        res = requests.post("http://localhost:1337/api/playlists", headers=POST_HEADERS, data=json_data)
        return res.text

class Video:
    def get_all(self):
        req = requests.get(url="http://localhost:1337/api/videos?populate=*", headers=HEADERS)
        return req.text.json()
    
    def get_by_id(self, video_id):
        req = requests.get(url=f"http://localhost:1337/api/playlist/{video_id}?populate=*", headers=HEADERS)
        return req.text
    
    def insert(self, video_data):
        json_data = json.dumps(video_data)
        res = requests.post("http://localhost:1337/api/videos", headers=POST_HEADERS, data=json_data, params={"populate":"playlists"})
        return res.text
    
