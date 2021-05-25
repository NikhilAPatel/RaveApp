from flask import (
    Flask,
    render_template,
    request,
    redirect,
    g
)
from flask_cors import CORS
from flask_socketio import (SocketIO, join_room, leave_room)
from random import(seed, randint)
from room import Room
import threading
import requests
import time
from datetime import datetime
import json
from urllib.parse import quote



# Create the application instance
app = Flask(__name__, template_folder="templates")
#socketio = SocketIO(app)
#CORS(app)

#  Client Keys
CLIENT_ID = "8457ff0a5bd847ccbb7b04886fd1bdf1"
CLIENT_SECRET = "85a731c048a34a97ba78b1937193057a"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = "code"
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}


# Create a URL route in our application for "/"
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/createRoom')
def create_room():
    cpm = request.args.get("cpm")
    colors = request.args.get("colors")

    rooms = get_rooms()

    # Generate room number
    room_number = randint(0, 1000000)
    while room_number in rooms.keys():
        room_number = randint(0, 1000000)

    dt = datetime.now()

    add_room(room_number, cpm, colors[1:].split("#"), dt.microsecond, False)

    return {
        "room_number": room_number,
    }


@app.route('/rave')
def start_rave():
    room_number = request.args.get("room_number")
    room = None
    rooms = get_rooms()

    # If this room does not exist, let the client know
    try:
        room = rooms[room_number]
    except(KeyError):
        return{
            "success": False,
            "room_number": room_number,
            "error": "value error"
        }

    except(ValueError):
        return{
            "success": False,
            "error": "value error"
        }

    return{
        "success": True,
        "colors": room[room_number]['colors'],
        "cpm": room[room_number]['cpm'],
        "created": room[room_number]['created']
    }


@app.route('/joinRoom')
def join_rave():
    room_number = request.args.get("room_number")
    rooms = get_rooms()

    # If this room does not exist, let the client know
    try:
        room = rooms[room_number]
    except(KeyError):
        return{
            "success": False
        }
    except(ValueError):
        return{
            "success": False
        }

    return{
        "success": True
    }


@app.route('/<room_number>')
def rave(room_number):
    return render_template('rave.html')

@app.route("/login")
def login():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
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
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)

    # Combine profile and playlist data to display
    display_arr = [profile_data] + playlist_data["items"]
    return render_template("loggedIn.html", sorted_array=display_arr)

# Redirect 404s to the home page
@app.errorhandler(404)
def fourOfour(request):
    return render_template('index.html')


def get_rooms():
    with open("rooms.txt", "r") as my_file_read:
        rooms = json.load(my_file_read)

    return rooms


def add_room(room_number, cpm, colors, created, dead):
    newRoom = {
        room_number: {
            'cpm': cpm,
            'colors': colors,
            'created': created,
            'dead': dead,
            'room_number': room_number
        }
    }

    rooms = get_rooms()
    rooms[room_number] = newRoom

    with open("rooms.txt", "w") as my_file:
        obj = json.dump(rooms, my_file)


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    seed(872340789023)
    app.run(debug=True)
