import json
import requests
from flask import request
import os

#  Client Keys
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://https://ravebynikhil.herokuapp.com"
PORT = 5000
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "user-read-currently-playing"
STATE = "code"
SHOW_DIALOG_bool = False
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

def spotify_login(code):
    # Auth Step 4: Requests refresh and access tokens
    auth_token = code
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    return  response_data["access_token"]

def get_features_data(access_token):
    id = currently_playing_id(access_token)
    authorization_header = {
        "Authorization": "Bearer {}".format(access_token)}

    if id == 0:
        return {
            "error": True,
            "message": "Not currently playing a song"
        }
    # Get Currently Playing Song Features
    features_api_endpoint = "https://api.spotify.com/v1/audio-features/"+id
    features_response = requests.get(
        features_api_endpoint, headers=authorization_header)
    features_data = json.loads(features_response.text)

    return features_data

def currently_playing_id(access_token):
    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {
        "Authorization": "Bearer {}".format(access_token)}

    try:
        # Get Currently Playing Data
        playing_api_endpoint = "https://api.spotify.com/v1/me/player/currently-playing"
        playing_response = requests.get(
            playing_api_endpoint, headers=authorization_header)
        playing_data = json.loads(playing_response.text)
    except:
        return 0

    return playing_data["item"]["id"]
