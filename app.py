from flask import (
    Flask,
    render_template,
    request
)
from flask_cors import CORS
from flask_socketio import (SocketIO, join_room, leave_room)
from random import(seed, randint)
from room import Room
import threading
import time
from datetime import datetime
import json


# Create the application instance
app = Flask(__name__, template_folder="templates")
socketio = SocketIO(app)
CORS(app)


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

    #If this room does not exist, let the client know
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
    rooms=get_rooms()
    
    #If this room does not exist, let the client know
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



#TODO
# Supposed to catch 404 errors
@app.errorhandler(404)
def fourOfour(request):
    return render_template('index.html')


def get_rooms():    
    with open("rooms.txt", "r") as my_file_read:
        rooms=json.load(my_file_read)
    
    return rooms

def add_room(room_number, cpm, colors, created, dead):
    newRoom={
        room_number:{
            'cpm': cpm,
            'colors': colors,
            'created': created,
            'dead': dead,
            'room_number': room_number
        }
    }

    rooms = get_rooms()
    rooms[room_number]=newRoom

    with open("rooms.txt", "w") as my_file:
        obj = json.dump(rooms, my_file)


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    seed(872340789023)
    app.run(debug=True)
