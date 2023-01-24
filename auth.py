import os
import json
from cryptography.fernet import Fernet
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/youtube']

def encode_data(data):
  fernet_key = os.getenv("FERNET_KEY")
  encoded_key = bytes(fernet_key, "utf-8")
  fernet = Fernet(encoded_key)
  return fernet.encrypt(bytes(data, "utf-8"))

def decode_data(encrypted):
  fernet_key = os.getenv("FERNET_KEY")
  encoded_key = bytes(fernet_key, "utf-8")
  fernet = Fernet(encoded_key)
  return fernet.decrypt(encrypted)

def format_env_to_secrets():
  if os.path.exists("secrets.txt"):
    print("secrets already set")
    return
  client_id = os.getenv("CLIENT_ID")
  project_id = os.getenv("PROJECT_ID")
  auth_uri = os.getenv("AUTH_URI")
  token_uri = os.getenv("TOKEN_URI")
  auth_provider_url = os.getenv("AUTH_PROVIDER_URL")
  client_secret = os.getenv("CLIENT_SECRET")
  redirect_uris = [os.getenv("REDIRECT_URIS")]

  formatted_obj = {
    "installed": {
      "client_id": client_id,
      "project_id": project_id,
      "auth_uri": auth_uri,
      "token_uri": token_uri,
      "auth_provider_x509_cert_url": auth_provider_url,
      "client_secret": client_secret,
      "redirect_uris": redirect_uris
    }
  }

  formatted_json = json.dumps(formatted_obj)
  encrypted = encode_data(formatted_json)
  with open("secrets.txt", "wb") as f:
    f.write(encrypted)

def get_client_config():
  f = open("secrets.txt")
  client_config = f.read()
  f.close()
  return json.loads(decode_data(client_config).decode("utf-8"))

def youtube_authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    return build("youtube", "v3", developerKey=os.getenv("API_KEY"))
