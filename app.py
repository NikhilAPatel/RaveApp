from flask import (
    Flask,
    render_template,
    request,
    redirect,
    g,
    session
)
from flask_cors import CORS
from flask_socketio import (SocketIO, join_room, leave_room)
from random import(seed, randint)
from room import *
import threading
import requests
import time
from datetime import datetime
import json
from urllib.parse import quote
from MLModel import ML_get_colors, ML_get_cpm
from spotify import *

# TODO hide api keys
# TODO change and hide secret key
# TODO if user tries to start a spotify rave but isn't playing any music, put up a splash page or something to tell them to start
# TODO make function for returning all of a rooms attributes (in JSON)
# TODO if a room code is less than 6 characters then you'll get a key error when searching for it
# TODO see if the Room class is still needed
# TODO make function for creating a unique room number
# TODO move all room related functions to a new file
# TODO move all the spotify variables to a new function
# TODO change the spotify callback so they go to the normal rave url "ravebynikhil.herokuapp.com/<room_number>"

# Create the application instance
app = Flask(__name__, template_folder="templates")
CORS(app)
app.secret_key = 'changethislater'

# Create a URL route in our application for "/"
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/createRoom')
def create_room():
    cpm = request.args.get("cpm")
    colors = request.args.get("colors")
    room_number = generate_room_number();
    
    dt = datetime.now()

    add_room(room_number, cpm, colors[1:].split(
        "#"), dt.microsecond, False, False)

    return {
        "room_number": room_number,
    }


@app.route('/rave')
def start_rave():
    room_number = request.args.get("room_number")
    return return_room(room_number)
    

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
    url_args = "&".join(["{}={}".format(key, quote(val))
                         for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/callback/q")
def callback():
    session['access_token'] = spotify_login(request.args['code'])
    return render_template("spotifyRave.html")


@app.route("/callback/startSpotifyRave")
def currently_playing():
    features_data = get_features_data(session['access_token'])
    id=currently_playing_id(session['access_token'])
    return {**{"id": id}, **ML_room_create(features_data)}


@app.route("/callback/currentlyPlayingId")
def return_currently_playing_id():
    return currently_playing_id(session['access_token'])


@app.route("/callback/checkNewSong")
def check_new_song():
    id = request.args.get("id")
    room_number = request.args.get("room_number")
    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {
        "Authorization": "Bearer {}".format(session['access_token'])}

    try:
        # Get Currently Playing Data
        playing_api_endpoint = "https://api.spotify.com/v1/me/player/currently-playing"
        playing_response = requests.get(
            playing_api_endpoint, headers=authorization_header)
        playing_data = json.loads(playing_response.text)
    except:
        return 0

    if(id != playing_data["item"]["id"]):
        return {**{"id": playing_data["item"]["id"]}, **ML_room_update(currently_playing(), room_number)}

    return {"newSong": False}


def ML_room_create(features_data):
    rooms = get_rooms()

    # Generate room number
    room_number = (str)(randint(0, 1000000))
    while room_number in rooms.keys():
        room_number = (str)(randint(0, 1000000))

    dt = datetime.now()

    add_room(room_number, ML_get_cpm(features_data), ML_get_colors(
        features_data)[1:], dt.microsecond, False, True)
    room = get_rooms()[(str)(room_number)]

    return{
        "success": True,
        "room_number": room_number,
        "colors": room[(str)(room_number)]['colors'],
        "cpm": room[(str)(room_number)]['cpm'],
        "created": room[(str)(room_number)]['created'],
        "version": room[(str)(room_number)]['version'],
        "room_number": (str)(room_number),
        "spotify_room": room[room_number]['spotify_room']
    }


def ML_room_update(features_data, room_number):
    rooms = get_rooms()
    update_room(room_number, ML_get_colors(
        features_data), ML_get_cpm(features_data))
    room = get_rooms()[(str)(room_number)]
    return{
        "success": True,
        "newSong": True,
        "room_number": room_number,
        "colors": room[(str)(room_number)]['colors'],
        "cpm": room[(str)(room_number)]['cpm'],
        "created": room[(str)(room_number)]['created'],
        "version": room[(str)(room_number)]['version'],
        "spotify_room": room[room_number]['spotify_room']
    }


@app.route("/updateRoom")
def updateRoom():
    room_number = request.args.get("room_number")
    rooms = get_rooms()
    room = rooms[room_number]
    return{
        "success": True,
        "newSong": True,
        "room_number": room_number,
        "colors": room[(str)(room_number)]['colors'],
        "cpm": room[(str)(room_number)]['cpm'],
        "created": room[(str)(room_number)]['created'],
        "version": room[(str)(room_number)]['version'],
        "spotify_room": room[room_number]['spotify_room']
    }

# TODO


@app.route("/checkupdate")
def checkupdate():
    return {
        "update": False
    }

# Redirect 404s to the home page


@app.errorhandler(404)
def fourOfour(request):
    return render_template('index.html')




# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    seed(872340789023)
    app.run(debug=True)
